# ==============================
# Imports
# ==============================
import streamlit as st
from fpdf import FPDF
from ai_diet_generator import generate_diet

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="AI Diet Planner",
    page_icon="🥗",
    layout="centered"
)

# ==============================
# Custom CSS (Modern UI)
# ==============================
st.markdown("""
<style>
body {
    background-color: #f0fdf4;
}
.main-title {
    font-size: 36px;
    font-weight: 700;
    color: #065f46;
    text-align: center;
}
.sub-title {
    text-align: center;
    color: #047857;
    margin-bottom: 30px;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #065f46;
    margin-bottom: 10px;
}
.output-box {
    background: #ecfdf5;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #10b981;
    white-space: pre-line;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# Helper: Clean text for PDF
# ==============================
def clean_text_for_pdf(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

# ==============================
# PDF Generator
# ==============================
def create_pdf(patient_id, diet_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Patient Diet Plan", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Patient ID: {patient_id}", ln=True)
    pdf.ln(5)

    safe_text = clean_text_for_pdf(diet_text)
    pdf.multi_cell(0, 8, safe_text)

    file_name = f"diet_plan_{patient_id}.pdf"
    pdf.output(file_name)
    return file_name

# ==============================
# UI Header
# ==============================
st.markdown('<div class="main-title">🥗 AI Diet Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Personalized diet plans using AI</div>', unsafe_allow_html=True)

# ==============================
# Input Card
# ==============================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Patient Details</div>', unsafe_allow_html=True)

    patient_id = st.text_input("Patient ID")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    weight = st.number_input("Weight (kg)", min_value=1.0, step=0.5)
    condition = st.selectbox(
        "Diet Type",
        ["Healthy", "Diabetic", "Weight Loss", "Heart Friendly"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# Generate Button
# ==============================
if st.button("✨ Generate Diet Plan", width="stretch"):
    if not patient_id:
        st.error("Please enter Patient ID")
    else:
        with st.spinner("Generating diet plan..."):
            diet_text = generate_diet(age, weight, condition)

        # Output
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Your Diet Plan</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="output-box">{diet_text}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # PDF
        pdf_file = create_pdf(patient_id, diet_text)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📄 Download Diet Plan (PDF)",
                data=f,
                file_name=pdf_file,
                mime="application/pdf",
                width="stretch"
            )

# ==============================
# Footer
# ==============================
st.markdown(
    "<p style='text-align:center; color:gray;'>Made for Medical OCR Project</p>",
    unsafe_allow_html=True
)
