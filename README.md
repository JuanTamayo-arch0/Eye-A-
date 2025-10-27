# 👁️ Eye(a) — AI-Powered Object Detection for Real-Time Security

> _"Turning surveillance cameras into intelligent observers."_

---

## 🧠 Overview

**Eye(a)** is a real-time **computer vision system** that enhances security monitoring using **deep learning**.  
The project leverages **YOLOv8** for object detection and **OpenCV** for image processing, enabling the identification of **weapons, fire, and other hazardous situations** through a live IP camera stream.

The model runs **locally or on a server**, providing **instant alerts** when dangerous objects are detected — improving both **response time** and **safety** in monitored environments.

---

## 🚨 Problem Statement

Despite the widespread presence of surveillance cameras, **most security systems remain passive**.  
Guards or operators must manually monitor multiple screens, leading to **delayed responses** or **missed incidents**.

Eye(a) proposes a **proactive AI system** capable of analyzing footage automatically,  
detecting threats in real-time, and issuing alerts before a human could react.

---

## 💡 Objectives

1. **Train a deep learning model** to recognize dangerous objects such as firearms, knives, and fire.  
2. **Integrate the model** into a real-time video processing system using OpenCV.  
3. **Develop a web-based interface** to simulate real-world security applications.  
4. Evaluate model performance through **precision**, **recall**, and **mAP** metrics.  
5. Propose **extensions for safety monitoring and automation**.

---

## 🧰 Tech Stack

| Category | Tools & Frameworks |
|-----------|-------------------|
| **Language** | ![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) |
| **Frameworks / Libraries** | ![Ultralytics](https://img.shields.io/badge/YOLOv8-Ultralytics-orange) ![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green?logo=opencv) |
| **Data Management** | ![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-lightblue?logo=pandas) ![OpenCSV](https://img.shields.io/badge/CSV-Data_Handling-lightgrey) |
| **Frontend / Visualization** | ![HTML](https://img.shields.io/badge/HTML-5-orange?logo=html5) ![CSS](https://img.shields.io/badge/CSS-3-blue?logo=css3) ![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript) |
| **Dataset Source** | ![Roboflow](https://img.shields.io/badge/Roboflow-Datasets-blueviolet?logo=roboflow) |
| **Version Control** | ![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github) |

---
# 📦 Installation & Setup

## 1️⃣ Clone the repository
```bash
git clone https://github.com/JuanTamayo-arch0/Eye-a.git
cd Eye-a
```

## 2️⃣ Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # (Mac/Linux)
venv\Scripts\activate      # (Windows)
```

## 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 4️⃣ Run the model with your camera feed
```bash
python main.py
```

You can replace your video source in the code:
```python
cap = cv2.VideoCapture("rtsp://your-ip-camera-url")
```

---

# 🤖 Model Training Details

We compared YOLOv8n (lightweight) and YOLOv8x (extended) versions.

## Datasets

| Object Type | Images | Resolution | Split (Train/Val/Test) |
|-------------|--------|------------|------------------------|
| Firearms    | 2,006  | 416x416    | 80/15/5                |
| Knives      | 858    | 416x416    | 70/20/10               |
| Fire        | 1,721  | 416x416    | 70/20/10               |
| Car Crash   | 1,509  | 416x416    | 87/8/5                 |

All datasets were preprocessed via Roboflow, annotated, and normalized for YOLO compatibility.

---

# 📊 Model Performance

| Model   | F1 Score | Precision | Recall | mAP@0.5 | Notes                      |
|---------|----------|-----------|--------|---------|----------------------------|
| YOLOv8n | 0.76     | 0.93      | 0.81   | 0.79    | Baseline model             |
| YOLOv8x | 0.77     | 0.97      | 0.85   | 0.82    | Better overall accuracy    |

## Key Findings:

* The YOLOv8x version achieved higher accuracy and lower confusion between similar classes (e.g., knives vs. background).
* The optimal confidence threshold was around 0.47, balancing precision and recall.
* The model's mAP@0.5:0.95 remained consistently above 0.75, indicating strong generalization.

---

# 🧮 Visual Performance Metrics

* 📉 **Loss Curves**: Both training and validation loss decreased steadily → no overfitting detected.
* 🎯 **Precision-Recall Curve**: Average precision across classes ranged from `0.75` to `0.87`.
* 📈 **F1-Confidence Curve**: Best performance achieved at confidence ≈ `0.47`.
* 🧩 **Confusion Matrix**: Most true positives lie on the diagonal; background confusion reduced in YOLOv8x.


# 🌍 Real-World Applications

* 🏫 Campus or building surveillance
* 🏠 Home or smart security systems
* 🏢 Commercial safety monitoring
* 👶 Infant safety systems (detecting small dangerous objects)
* 🚨 Crowd event monitoring and alert automation

---

# 🧭 Future Improvements

* Expand dataset for additional hazard categories (e.g., explosives, smoke, glass breaking).
* Develop a lightweight edge-compatible version for deployment on Raspberry Pi or Jetson Nano.
* Integrate with IoT notification systems (e.g., Telegram or Twilio alerts).
* Implement a dashboard for analytics and log tracking.
* Introduce multi-class tracking using DeepSORT or ByteTrack.

---

# 📚 References

* [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
* [OpenCV Official Documentation](https://docs.opencv.org/)
* [Roboflow – Computer Vision Datasets](https://roboflow.com/)
* [mAP Explained – Papers with Code](https://paperswithcode.com/)

---

<p align="center">
Developed with by <b>Juan José Tamayo</b> 
<i>Empowering safety through intelligent vision.</i>
</p>

