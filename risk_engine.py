# risk_engine.py

RISK_SCORES = {
    "person": 5,
    "knife": 70,
    "scissors": 50,
    "baseball bat": 40,
    "cell phone": 5,   # Temporary hackathon fix
    "backpack": 5,
    "car": 10,
    "truck": 15,
    "motorcycle": 10
}

def calculate_risk(detected_objects):

    unique_objects = list(set(detected_objects))

    
    score = 0

    for obj in unique_objects:
        score += RISK_SCORES.get(obj, 0)

    if score >= 60:
        level = "HIGH RISK"
    elif score >= 30:
        level = "MEDIUM RISK"
    else:
        level = "LOW RISK"

    return score, level, unique_objects