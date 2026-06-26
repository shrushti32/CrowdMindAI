from flask import Flask, render_template
import csv
import os
import json


app = Flask(__name__)

LOG_FILE = "incident_log.csv"


@app.route("/")
def home():

    incidents = []

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as file:

            reader = csv.reader(file)

            next(reader)

            for row in reader:
                incidents.append(row)

    incidents.reverse()

    # Read live status
    if os.path.exists("live_status.json"):
        with open("live_status.json", "r") as file:
            status = json.load(file)
    else:
        status = {
            "risk_score": 0,
            "risk_level": "LOW RISK",
            "objects": [],
            "people_count": 0
        }

    return render_template(
        "index.html",
        incidents=incidents,
        status=status
    )
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)