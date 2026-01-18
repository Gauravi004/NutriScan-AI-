from google import genai
import json
import streamlit as st

# ==============================
# Create Gemini Client
# ==============================
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# ==============================
# Diet Generator Function
# ==============================
def generate_diet(patient_id):
    with open("final_diet_output.json", "r") as f:
        patients = json.load(f)

    patient = next((p for p in patients if int(p["patient_id"]) == patient_id), None)
    if not patient:
        return None

    disease = patient["bert_prediction"]

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

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    diet_text = response.text
    return {"diet_plan": diet_text}
