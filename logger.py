# logger.py

import os
import csv
import cv2
from datetime import datetime

# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)

LOG_FILE = "incident_log.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Date",
            "Time",
            "Risk Score",
            "Risk Level",
            "Objects"
        ])


def save_incident(frame, risk_score, risk_level, objects):

    # Generate image filename
    filename = datetime.now().strftime(
        "screenshots/%Y-%m-%d_%H-%M-%S.jpg"
    )

    # Save screenshot
    cv2.imwrite(filename, frame)

    # Save log
    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%d-%m-%Y"),
            datetime.now().strftime("%H:%M:%S"),
            risk_score,
            risk_level,
            ", ".join(objects)
        ])

    print(f"[INFO] Incident Saved -> {filename}")