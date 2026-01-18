import json
import os
from google import genai

# ==============================
# Gemini Client Setup
# ==============================
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# ==============================
# Diet Generator Function
# ==============================
def generate_diet(patient_id):

    # -------- Load patient data --------
    with open("final_diet_output.json", "r", encoding="utf-8") as f:
        patients = json.load(f)

    patient = next((p for p in patients if str(p["patient_id"]) == str(patient_id)), None)

    if not patient:
        return None

    disease = patient.get("bert_prediction", "General Health")

    # ==============================
    # PROMPT (AS YOU ASKED)
    # ==============================
    prompt = f"""
You are a clinical dietitian.

Generate a 2-day diet plan.

Patient ID: {patient_id}
Medical Condition: {disease}

FORMAT:

Day 1:
Breakfast:
Lunch:
Snack:
Dinner:

Day 2:
Breakfast:
Lunch:
Snack:
Dinner:
"""

    # -------- Gemini Call --------
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents=prompt
    )

    return response.text
