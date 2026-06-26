from alert_engine import play_alert
from ultralytics import YOLO
import cv2
import csv
import time
import json

from risk_engine import calculate_risk
from logger import save_incident

# Load YOLO Model
model = YOLO("yolov8s.pt")

# Open Camera
cap = cv2.VideoCapture(0)

# To avoid saving too many screenshots
last_saved_time = 0
def get_incident_count():
    try:
        with open("incident_log.csv", "r") as file:
            return max(0, sum(1 for row in file) - 1)
    except:
        return 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # YOLO Detection
    results = model(frame)

    detected_objects = []
    person_box = None
    knife_box = None

    for box in results[0].boxes:

        conf = float(box.conf[0])

        # Ignore low confidence detections
        if conf < 0.60:
            continue

        cls = int(box.cls[0])
        name = model.names[cls]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if name == "person":
            person_box = (x1, y1, x2, y2)

        if name == "knife":
            knife_box = (x1, y1, x2, y2)

        detected_objects.append(name)

    # Risk Calculation
    risk_score, risk_level, unique_objects = calculate_risk(detected_objects)

    # -------- Threat Proximity Check --------
    # If both person and knife are detected, raise critical alert
    if person_box is not None and knife_box is not None:
     risk_score = 100
     risk_level = "CRITICAL"

   
    # Count people
    people_count = detected_objects.count("person")

    # Save live status
    live_status = {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "objects": unique_objects,
        "people_count": people_count
    }

    with open("live_status.json", "w") as file:
        json.dump(live_status, file, indent=4)

    # Draw detections
    annotated_frame = results[0].plot()

    if risk_score >= 60:

     play_alert()

     cv2.rectangle(
        annotated_frame,
        (0, 0),
        (annotated_frame.shape[1], annotated_frame.shape[0]),
        (0, 0, 255),
        8
    )
    if risk_level in ["HIGH RISK", "CRITICAL"]:
     cv2.rectangle(
        annotated_frame,
        (0, 0),
        (annotated_frame.shape[1], annotated_frame.shape[0]),
        (0, 0, 255),
        8
    )

    cv2.putText(
        annotated_frame,
        f"Risk Score : {risk_score}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    if risk_level == "LOW RISK":
     risk_color = (0, 255, 0)

    elif risk_level == "MEDIUM RISK":
     risk_color = (0, 255, 255)

    elif risk_level == "HIGH RISK":
     risk_color = (0, 165, 255)

    else:
     risk_color = (0, 0, 255)

    cv2.putText(
    annotated_frame,
    f"Risk : {risk_level}",
    (20, 70),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    risk_color,
    2
)
    # Show People Count
    cv2.putText(
     annotated_frame,
     f"People : {people_count}",
     (20, 175),
     cv2.FONT_HERSHEY_SIMPLEX,
     0.8,
     (255, 255, 255),
     2
    )
    
    cv2.putText(
        annotated_frame,
        f"Objects : {len(unique_objects)}",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    current_clock = time.strftime("%H:%M:%S")

    cv2.putText(
        annotated_frame,
        current_clock,
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Critical Alert
    if risk_level in ["HIGH RISK", "CRITICAL"]:

        cv2.putText(
            annotated_frame,
            "POTENTIAL ATTACK DETECTED!",
            (250, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            3
        )
    current_time = time.time()

    if current_time - last_saved_time > 30:
        if risk_level in ["HIGH RISK", "CRITICAL"]:

            save_incident(
                annotated_frame,
                risk_score,
                risk_level,
                unique_objects
            )

            last_saved_time = current_time

    incident_count = get_incident_count()
    
    cv2.putText(
    annotated_frame,
    "SYSTEM STATUS : ACTIVE",
    (20, 420),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)
    cv2.imshow("CrowdMind AI", annotated_frame) 
    cv2.putText(
    annotated_frame,
    "CrowdMind AI - Smart Public Safety System",
    (20, 380),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (255, 255, 0),
    2
)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()