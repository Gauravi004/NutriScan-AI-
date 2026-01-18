# ==============================
# Imports
# ==============================
import os
st.write(os.listdir("assets"))

import streamlit as st
from fpdf import FPDF
from ai_diet_generator import generate_diet
import re

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="AI Diet Planner",
    page_icon="🥗",
    layout="wide"
)

# ==============================
# Custom CSS (Improved UI)
# ==============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f1e1c, #1c2f28);
    color: #e0ffe0;
    font-family: 'Segoe UI', sans-serif;
}
.stApp h1 {
    color: #34d399;
    text-align: center;
    font-size: 44px;
    margin-bottom: 10px;
}
.sub-card {
    background: linear-gradient(135deg, #1f3d28, #244a33);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.4);
    text-align: center;
    font-size: 16px;
}
.sub-card span {
    color: #6ee7b7;
    font-size: 14px;
}
.diet-card {
    background-color: #1f3d28;
    color: #e0ffe0;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 3px 3px 14px rgba(0,0,0,0.35);
    font-size: 16px;
    line-height: 1.8;
}
div.stButton > button {
    background: linear-gradient(90deg, #10b981, #34d399);
    color: white;
    font-size: 18px;
    padding: 10px 28px;
    border-radius: 14px;
    border: none;
}
.stTextInput input {
    border-radius: 14px;
    padding: 10px;
    border: 2px solid #10b981;
    background-color: #0f1e1c;
    color: #e0ffe0;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================
# Helpers
# ==============================
def remove_emojis(text):
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub("", text)

def extract_disease(text):
    match = re.search(r"(disease|condition)\s*:\s*(.+)", text, re.IGNORECASE)
    return match.group(2).strip() if match else "Not Specified"

# ==============================
# PDF Generator
# ==============================
def create_pdf(patient_id, diet_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Diet Plan", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    safe_text = remove_emojis(diet_text).encode("latin1", "replace").decode("latin1")

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    file_name = f"diet_plan_{patient_id}.pdf"
    pdf.output(file_name)
    return file_name

# ==============================
# Title
# ==============================
st.title("🥗 AI Diet Planner 🍎")
st.caption("Personalized nutrition made simple & smart")

st.image(
    "assets/main.jpg",
    use_container_width=True
)

# ==============================
# Layout
# ==============================
col1, col2 = st.columns([2, 1])

with col1:
    patient_id = st.text_input("Enter Patient ID", placeholder="e.g. 101")

    if st.button("Generate Diet Plan"):
        if patient_id.isdigit():
            with st.spinner("Generating diet plan..."):
                diet_text = generate_diet(patient_id)

            if diet_text:
                st.success("✅ Diet Generated Successfully!")

                disease = extract_disease(diet_text)

                # 🔹 Patient Info Cards
                info1, info2 = st.columns(2)
                with info1:
                    st.markdown(f"""
                    <div class="sub-card">
                        <span>Patient ID</span><br>
                        <b>{patient_id}</b>
                    </div>
                    """, unsafe_allow_html=True)

                with info2:
                    st.markdown(f"""
                    <div class="sub-card">
                        <span>Medical Condition</span><br>
                        <b>{disease}</b>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("Your Diet Plan 🥗")

                # 🔹 Day-wise Diet Cards
                for block in diet_text.split("\n\n"):
                    st.markdown(f"""
                        <div class="diet-card">
                            {block.replace("\n", "<br>")}
                        </div>
                    """, unsafe_allow_html=True)

                # PDF
                pdf = create_pdf(patient_id, diet_text)
                with open(pdf, "rb") as f:
                    st.download_button(
                        "📄 Download PDF",
                        f,
                        file_name=pdf,
                        mime="application/pdf"
                    )
            else:
                st.error("❌ Diet generation failed")
        else:
            st.warning("⚠️ Enter numeric ID only")

with col2:
    st.image(
        "assets/second.jpg",
        use_container_width=True
    )
    st.caption("Healthy Eating = Healthy Life 🥗")

# ==============================
# Footer
# ==============================
st.markdown("""
<div style="text-align:center; font-size:14px; margin-top:30px; color:#6ee7b7;">
💡 Tip: Drink water regularly & walk 30 minutes daily
</div>
""", unsafe_allow_html=True)



