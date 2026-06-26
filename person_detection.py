import os
import csv
import time
from datetime import datetime
from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)

# Create incident log file
log_file = "incident_log.csv"

if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Time", "Risk Score", "Objects"])

# Risk scores
risk_scores = {
    "person": 5,
    "knife": 70,
    "baseball bat": 40,
    "scissors": 30,
    "backpack": 5,
    "car": 10,
    "truck": 15
}

# Open camera
cap = cv2.VideoCapture(0)

last_capture_time = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    detected_objects = []
    risk = 0

    for box in results[0].boxes:
        cls = int(box.cls[0])
        name = model.names[cls]

        detected_objects.append(name)

        if name in risk_scores:
            risk += risk_scores[name]

    # Draw detection boxes
    annotated_frame = results[0].plot()

    # Default risk level
    level = "LOW RISK"


    # Decide Risk Level
    if risk > 60:
        level = "HIGH RISK"

        current_time = time.time()

        # Save screenshot every 5 seconds
        if current_time - last_capture_time > 5:

            filename = datetime.now().strftime(
                "screenshots/%Y-%m-%d_%H-%M-%S.jpg"
            )

            cv2.imwrite(filename, annotated_frame)
            print(f"Screenshot Saved: {filename}")

            # Save incident to CSV
            with open(log_file, "a", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    datetime.now().strftime("%d-%m-%Y"),
                    datetime.now().strftime("%H:%M:%S"),
                    risk,
                    ", ".join(set(detected_objects))
                ])

            last_capture_time = current_time

    elif risk > 30:
        level = "MEDIUM RISK"

    else:
        level = "LOW RISK"

    # Display Risk Score
    cv2.putText(
        annotated_frame,
        f"Risk Score: {risk}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # Display Risk Level
    cv2.putText(
        annotated_frame,
        level,
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.imshow("CrowdMind AI", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
