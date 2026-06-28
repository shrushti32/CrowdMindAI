🚨 CrowdMindAI - Smart Public Safety System

   Feedback form link 
   https://docs.google.com/forms/d/19i9JVj_1ZKKFbvS9FcEiua7HCZ01mS7Q3eYfWtBMN80/edit#responses

📌 Project Overview
CrowdMindAI is an AI-based smart surveillance system designed to detect dangerous situations like violence, weapon presence, and abnormal crowd behavior in real-time using computer vision.

The system uses YOLO-based object detection and a custom risk analysis engine to generate instant alerts and improve public safety.

---

🎯 Features
- Real-time person detection
- Weapon detection (knife, etc.)
- Crowd behavior monitoring
- Risk level analysis (Low / Medium / High)
- Live alert generation
- Incident logging system
- Live status tracking using JSON
- Demo video support for presentation

---

🧠 Tech Stack
- Python
- OpenCV
- YOLOv8 (Ultralytics)
- Flask (if used in app)
- NumPy
- JSON / CSV logging

---

📂 Project Structure
- `app.py` → Main application
- `alert_engine.py` → Generates alerts
- `risk_engine.py` → Calculates risk level
- `person_detection.py` → Detects people & objects
- `logger.py` → Stores incidents
- `live_status.json` → Real-time status data
- `incident_log.csv` → Event logs
- `yolov8s.pt` → AI detection model

---
⚙️ How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the project
python app.py
