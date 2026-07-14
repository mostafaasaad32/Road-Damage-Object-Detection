# 🛡️ RoadGuard Pro: Autonomous Road Damage Detection

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://road-damage-object-detection-xwzzhshderxk7ayv8kmdcp.streamlit.app/)
[![Dataset: Roboflow](https://img.shields.io/badge/Dataset-Roboflow%20Road%20Damage-purple?style=flat-square&logo=roboflow)](https://universe.roboflow.com/trafficsignssafeway/road-damage-l1ju7/browse)
[![Model: Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-YOLOv8m%20Road%20Crack%20Detection-ffd21e?style=flat-square)](https://huggingface.co/mostafaasaad32/yolo_road_crack_detection)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Ultralytics YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-00ffff?style=flat-square)](https://github.com/ultralytics/ultralytics)

**RoadGuard Pro** is an autonomous, high-precision road infrastructure inspection platform powered by state-of-the-art **YOLOv8** deep learning architectures. It detects, classifies, and evaluates pavement degradation in real-time, enabling municipalities, highway authorities, and autonomous inspection vehicles to prioritize road maintenance effectively.

---

## 🔗 Quick Links

- **🚀 Live Streamlit Web Application:** [RoadGuard Pro Live App](https://road-damage-object-detection-xwzzhshderxk7ayv8kmdcp.streamlit.app/)
- **📊 Dataset Exploration & Download:** [Roboflow Road Damage Dataset](https://universe.roboflow.com/trafficsignssafeway/road-damage-l1ju7/browse)
- **🧠 Pre-trained Model Weights:** [Hugging Face Model Hub (`mostafaasaad32/yolo_road_crack_detection`)](https://huggingface.co/mostafaasaad32/yolo_road_crack_detection)

---

## ✨ Key Features

- **🏆 Production-Grade YOLOv8m Engine:** Dedicated to the highest-performing **YOLOv8m (Medium)** model (`best_overall_model`), achieving **57.74% mAP50** and **62.59% Precision** while running at real-time speeds (>33 FPS).
- **🖼️ Multi-Class Road Damage Detection:** Accurately identifies and localizes 5 critical categories of road surface distress:
  - `Longitudinal Crack`
  - `Transverse Crack`
  - `Alligator Crack`
  - `Other Corruption`
  - `Pothole`
- **📊 Interactive Comparative Dashboard:** Built-in dashboard with Plotly data visualizations comparing architectural trade-offs between `YOLOv8n (Nano)`, `YOLOv8s (Small)`, and `YOLOv8m (Medium)`.
- **🚨 Automated Severity Assessment:** Calculates a composite **Road Severity Index (0–100)** for inspected imagery and categorizes road conditions (`Excellent`, `Moderate`, `Severe`, `Critical`).
- **📦 Batch Inspection & Reporting:** Upload multiple road images simultaneously for automated batch inspection and export comprehensive CSV inspection reports with bounding boxes, confidence scores, and severity ratings.
- **🎨 Sleek Dark-Mode Glassmorphism UI:** Designed with modern aesthetics, custom CSS styling, and responsive layout structure.

---

## 📈 Model Performance & Evaluation

During our extensive architectural exploration using the **RDD2022 / Roboflow Road Damage Dataset**, three variants of **YOLOv8** were trained and benchmarked. **YOLOv8m (Medium)** emerged as the undisputed leader in accuracy while exceeding the 30 FPS real-time benchmark.

### Comparative Evaluation Matrix

| Model | mAP50 | mAP50-95 | Precision | Recall | Parameters / Size | Latency | Inference Speed | Selection |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLOv8n (Nano)** | 51.26% | 25.87% | 57.69% | 48.46% | ~3.0M / 5.96 MB | 14.10 ms | 70.91 FPS | Edge / IoT Baseline |
| **YOLOv8s (Small)** | 56.04% | 28.98% | 59.88% | 54.26% | ~11.2M / 21.47 MB | 20.03 ms | 49.92 FPS | Balanced |
| **YOLOv8m (Medium)** | **57.74%** | **30.18%** | **62.59%** | **54.56%** | **~25.9M / 49.62 MB** | **30.08 ms** | **33.24 FPS** | **🏆 Best Overall Model** |

### Why YOLOv8m?
Detecting hairline asphalt cracks and complex alligator cracking requires capturing subtle texture differentials across multi-scale feature maps. The higher capacity of `YOLOv8m` (`~25.9M parameters`) delivers a **+6.48% jump in mAP50** and **+4.90% jump in Precision** over Nano, virtually eliminating false positives caused by shadows, pavement joints, and oil stains.

---

## 🗂️ Project Structure

```text
├── app.py                             # Main Streamlit web application
├── model_utils.py                     # Model loading, Hugging Face weight downloader & inference utilities
├── styles.py                          # Custom CSS styling (Dark-Mode Glassmorphism UI)
├── data.yaml                          # Dataset configuration and class definition file
├── Final_Models_Comparison.csv        # Benchmark evaluation metrics across YOLOv8 variants
├── requirements.txt                   # Python dependencies for local and cloud deployment
├── road-damage-object-detection.ipynb # Complete training, evaluation & experimentation notebook
└── README.md                          # Project documentation
```

---

## 💻 Local Setup & Installation

Follow these steps to run the application locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/road-damage-object-detection.git
cd road-damage-object-detection
```

### 2. Create a Virtual Environment (Recommended)
```bash
# Using venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Application
```bash
streamlit run app.py
```
Once launched, open your web browser and navigate to `http://localhost:8501`.

---

## 🤖 Model Weights Management

To maintain a lightweight Git repository suitable for cloud deployments, the trained **YOLOv8m** weights (`best.pt`) are hosted on the **Hugging Face Hub**. When `app.py` is executed, `model_utils.py` automatically downloads the weights (`~49.6 MB`) and caches them locally in the `models/` directory:

- **Repository:** `mostafaasaad32/yolo_road_crack_detection`
- **Filename:** `best.pt`

---

## 📊 Dataset Information

The model was trained on the **Road Damage Dataset**, featuring annotated images across varied illumination, weather, and pavement conditions.
- **Explore & Download the Dataset:** [Roboflow Universe - Road Damage Dataset](https://universe.roboflow.com/trafficsignssafeway/road-damage-l1ju7/browse)
- **Classes Included:** `longitudinal crack`, `transverse crack`, `alligator crack`, `other corruption`, `pothole`.

---

## 🛠️ Built With

- **[Streamlit](https://streamlit.io/)**: Interactive web dashboard framework.
- **[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)**: Real-time object detection architecture.
- **[OpenCV & PIL](https://opencv.org/)**: Image processing and bounding box rendering.
- **[Plotly](https://plotly.com/python/)**: Interactive data visualization charts.
- **[Hugging Face Hub](https://huggingface.co/)**: Cloud hosting and caching for neural network weights.

---

## 📝 License

This project is open-source and available under the **MIT License**.
