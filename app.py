# ==============================
# Imports
# ==============================
import streamlit as st
from fpdf import FPDF
from ai_diet_generator import generate_diet

# ==============================
# Custom CSS
# ==============================
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #0f1e1c, #192924);
    color: #e0ffe0;
    font-family: 'Segoe UI', sans-serif;
}
.stApp h1 {
    color: #00ff7f;
    text-align: center;
    font-size: 42px;
    margin-bottom: 20px;
}
div.stButton > button {
    background: linear-gradient(90deg, #10b981, #34d399);
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 12px;
    border: none;
    margin-top: 10px;
}
.stTextInput input {
    border-radius: 12px;
    padding: 10px;
    border: 2px solid #10b981;
    background-color: #0f1e1c;
    color: #e0ffe0;
}
.diet-card {
    background-color: #1f3d28;
    color: #e0ffe0;
    padding: 18px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.4);
    font-size: 16px;
    line-height: 1.6;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================
# PDF Generator (Unicode-safe)
# ==============================
class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "AI Diet Plan", 0, 1, "C")
        self.ln(5)

def create_pdf(patient_id, diet_text):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add DejaVuSans font (supports Unicode & emojis)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 12)

    for line in diet_text.split("\n"):
        line = line.strip()
        if line:
            pdf.multi_cell(0, 8, line)

    file_name = f"diet_plan_{patient_id}.pdf"
    pdf.output(file_name)
    return file_name

# ==============================
# Title & Banner
# ==============================
st.title("🥗 AI Diet Planner 🍎")
st.image(
    "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
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

                # Separate meals
                meals = {
                    "Breakfast 🥣": "",
                    "Lunch 🥗": "",
                    "Snacks 🍎": "",
                    "Dinner 🍛": ""
                }

                current_meal = None
                for raw_line in diet_text.split("\n"):
                    line = raw_line.strip()
                    lower = line.lower()

                    if lower.startswith("breakfast"):
                        current_meal = "Breakfast 🥣"
                        continue
                    if lower.startswith("lunch"):
                        current_meal = "Lunch 🥗"
                        continue
                    if lower.startswith("snack"):
                        current_meal = "Snacks 🍎"
                        continue
                    if lower.startswith("dinner"):
                        current_meal = "Dinner 🍛"
                        continue

                    if current_meal and line:
                        meals[current_meal] += f"- {line}<br>"

                # Display meals
                st.subheader("Your Diet Plan 🥗")
                for meal, content in meals.items():
                    if content:
                        st.markdown(f"""
                            <div class="diet-card">
                                <b>{meal}</b><br><br>
                                {content}
                            </div>
                        """, unsafe_allow_html=True)

                # Create PDF
                pdf_file = create_pdf(patient_id, diet_text)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "📄 Download PDF",
                        f,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )

            else:
                st.error("❌ Diet generation failed. Try again.")

        else:
            st.warning("⚠️ Enter numeric Patient ID only")

with col2:
    st.image(
        "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce",
        use_container_width=True
    )
    st.caption("Healthy Eating = Healthy Life 🥗")

# ==============================
# Footer
# ==============================
st.markdown("""
<div style="text-align:center; font-size:14px; margin-top:20px; color:#00ff7f;">
💡 Tip: Drink water & walk 30 minutes daily
</div>
""", unsafe_allow_html=True)
