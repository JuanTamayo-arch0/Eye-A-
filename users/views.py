# Import basic libs

from datetime import datetime
from io import BytesIO
import tempfile
import uuid
import time
import cv2
import os


# Import django libs

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import StreamingHttpResponse, FileResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
from .forms import CustomUserCreationForm, CameraForm, CameraSettingsForm
from .models import Camera, CameraImage, Alerta

# Import yolo libs

from ultralytics.utils.plotting import Annotator
from ultralytics import YOLO

# Global varaibles

last_capture_time = 0


# login and register views

def register_view(request):
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            print('Funciono')
            return redirect('home') 
        else:
            messages.error(request, 'Verifica los datos ingresados')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print("Si funcionooo")
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'users/login.html')

# Home_view

def home_view(request):
    camaras = Camera.objects.filter(usuario=request.user)
    return render(request, 'users/home.html', {'camaras': camaras})

def nueva_camara_view(request):
    if request.method == 'POST':
        form = CameraForm(request.POST)
        if form.is_valid():
            camara = form.save(commit=False)
            camara.usuario = request.user
            camara.save()
            return redirect('home')
    else:
        form = CameraForm()
    return render(request, 'users/nueva_camara.html', {'form': form})

def eliminar_camara_view(request, camara_id):
    camara = get_object_or_404(Camera, id=camara_id, usuario=request.user)
    camara.delete()
    return redirect('home')

def galeria_camara_view(request, camara_id):
    camara = Camera.objects.get(id=camara_id)
    alertas = Alerta.objects.filter(camara=camara).order_by('-fecha_deteccion')[:10]
    if request.method == 'POST':
        form = CameraSettingsForm(request.POST, instance=camara)
        if form.is_valid():
            form.save()
            return redirect('galeria_camara', camara_id=camara.id)
    else:
        form = CameraSettingsForm(instance=camara)
    return render(request, 'users/cam.html', {'camara': camara, 'alertas': alertas, 'form': form})

# Model things and functions

model = YOLO("runs/detect/train27/weights/best.pt") 
DEVICE = "cuda"

def detect_objects(frame, camara_id):
    global last_capture_time
    camara = get_object_or_404(Camera, id=camara_id)
    results = model(frame, device=DEVICE)
    result = results[0]
    boxes = result.boxes
    capture_delay = camara.intervalo_captura

    nombres_detectados = []

    if boxes is not None:
        boxes = boxes[boxes.conf >= camara.certeza_minima]
        result.boxes = boxes

        for box in boxes:
            class_id = int(box.cls[0].item())
            class_name = model.names[class_id]
            nombres_detectados.append(class_name)

        if nombres_detectados:
            current_time = time.time()
            if current_time - last_capture_time >= capture_delay:
                _, buffer = cv2.imencode('.jpg', frame)
                image_stream = BytesIO(buffer)

                for deteccion in set(nombres_detectados):
                    alerta = Alerta(
                        camara_id=camara_id,
                        tipo_deteccion=deteccion
                    )
                    alerta.imagen.save(f"{deteccion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg", ContentFile(image_stream.getvalue()), save=True)
                last_capture_time = current_time

            print((current_time - last_capture_time))
            
    return result.plot()


def generar_stream(camara_ip, camara_id):

    ip = "http://"+camara_ip+":8080/video"

    print(ip)

    cap = cv2.VideoCapture(ip)
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = detect_objects(frame,camara_id)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def video_feed(request, camara_id):
    camara = get_object_or_404(Camera, id=camara_id, usuario=request.user)
    return StreamingHttpResponse(generar_stream(camara.ip, camara.id), content_type='multipart/x-mixed-replace; boundary=frame')


def obtener_alerta(request, camara_id):
    alerta = alertas_por_camara.get(camara_id, "Sin detecciones")
    print(alertas_por_camara)
    return JsonResponse({'alerta': alerta})

def ver_alertas(request, camara_id):
    camara = Camera.objects.get(id=camara_id)
    alertas = Alerta.objects.filter(camara=camara).order_by('-fecha_deteccion')
    return render(request, 'users/alertas.html', {'camara': camara, 'alertas': alertas})

# Test functions

def procesar_imagen_temporal(path):
    img = cv2.imread(path)
    results = model(img, device=DEVICE)
    result = results[0].plot()
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False, dir=os.path.join(settings.MEDIA_ROOT, "temp"))
    cv2.imwrite(temp_file.name, result)
    return temp_file.name

def procesar_video_temporal(path):
    cap = cv2.VideoCapture(path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False, dir=os.path.join(settings.MEDIA_ROOT, "temp")).name

    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, device=DEVICE)
        processed = results[0].plot()
        out.write(processed)

    cap.release()
    out.release()
    return out_path

def test_modelo(request):
    original_url = None
    resultado_url = None
    es_video = False

    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        filename = str(uuid.uuid4()) + "_" + archivo.name
        temp_path = os.path.join(settings.MEDIA_ROOT, "temp", filename)

        # Guardar archivo temporalmente
        with open(temp_path, 'wb+') as dest:
            for chunk in archivo.chunks():
                dest.write(chunk)

        if archivo.content_type.startswith('image'):
            procesado_path = procesar_imagen_temporal(temp_path)
        elif archivo.content_type.startswith('video'):
            raw = procesar_video_temporal(temp_path)
            procesado_path = ""
            procesado_path = reencode_to_h264(raw)
            es_video = True
        else:
            return render(request, 'test_model.html', {'error': 'Formato no soportado'})

        # Convertimos ruta absoluta a URL accesible por el navegador
        original_url = settings.MEDIA_URL + "temp/" + os.path.basename(temp_path)
        resultado_url = settings.MEDIA_URL + "temp/" + os.path.basename(procesado_path)

    return render(request, 'users/test_model.html', {
        'original_url': original_url,
        'resultado_url': resultado_url,
        'es_video': es_video
    })


import subprocess

def reencode_to_h264(input_path):
    output_path = input_path.replace(".mp4", "_h264.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-vcodec", "libx264", "-preset", "fast",
        "-crf", "23", output_path
    ])
    return output_path