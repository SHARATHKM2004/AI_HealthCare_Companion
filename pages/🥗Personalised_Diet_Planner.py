import streamlit as st
from fpdf import FPDF
import datetime
from tempfile import NamedTemporaryFile
from PIL import Image

# Sample symptoms and their associated dietary recommendations
diet_recommendations = {
    "Cough": [
        "Warm soups with garlic and ginger",
        "Honey and lemon tea",
        "Avoid cold foods and drinks",
        "Increase vitamin C intake through fruits like oranges and strawberries",
        "Drink turmeric milk to soothe the throat",
        "Steam inhalation with herbs like eucalyptus or peppermint"
    ],
    "Shortness of Breath": [
        "Increase intake of iron-rich foods (spinach, lentils, red meat)",
        "Vitamin B12-rich foods like eggs and dairy products",
        "Avoid processed foods and high-sodium meals",
        "Stay hydrated",
        "Include foods rich in omega-3 fatty acids (salmon, flaxseeds, walnuts)",
        "Add potassium-rich foods like bananas and sweet potatoes to your diet"
    ],
     "Chest Pain": [
        "Foods rich in omega-3 (salmon, walnuts, chia seeds)",
        "Reduce caffeine and alcohol intake",
        "Low-sodium foods to support heart health",
        "Incorporate fruits and vegetables rich in antioxidants",
        "Whole grains like oats and quinoa for heart health",
        "Avoid saturated fats and trans fats found in fried and processed foods"
    ],
    "Nausea": [
        "Ginger tea or ginger-based foods",
        "Small, frequent meals with low-fat foods",
        "Avoid spicy, fried, and acidic foods",
        "Include dry foods like toast or crackers",
        "Suck on peppermint candies or drink peppermint tea",
        "Cold foods like yogurt or popsicles can help settle the stomach"
    ],
    "Vomiting": [
        "Clear fluids like water, apple juice, and broth",
        "Bananas, rice, applesauce, and toast (BRAT diet)",
        "Avoid dairy products temporarily",
        "Increase hydration with electrolyte-rich drinks",
        "Plain boiled potatoes or carrots for gentle digestion",
        "Sip on ginger ale or ginger tea to ease nausea"
    ],
    "Diarrhea": [
        "BRAT diet: bananas, rice, applesauce, and toast",
        "Avoid dairy, caffeine, and high-fiber foods",
        "Increase water intake to prevent dehydration",
        "Plain chicken or turkey, cooked carrots, and potatoes",
        "Consume probiotic-rich foods like yogurt or kefir (if tolerated)",
        "Drink coconut water to replenish electrolytes"
    ],
    "Fever": [
        "Hydrate with water, herbal teas, and clear broths",
        "Foods high in protein to maintain strength (eggs, lean meats)",
        "Include immune-boosting foods like citrus fruits and leafy greens",
        "Avoid fatty, greasy, and high-sugar foods",
        "Soups with garlic, ginger, and turmeric for anti-inflammatory benefits",
        "Eat soft, easy-to-digest foods like porridge or mashed potatoes"
    ],
    "Fatigue": [
        "Whole grains (brown rice, oats) for sustained energy",
        "Nuts and seeds for healthy fats and proteins",
        "Green leafy vegetables for iron and magnesium",
        "Avoid excessive caffeine and sugar to prevent energy crashes",
        "Protein-rich foods like beans, lentils, and eggs",
        "Add superfoods like spirulina, chia seeds, and berries to your meals"
    ],
    "Headache": [
        "Hydrate with plenty of water",
        "Magnesium-rich foods like almonds, avocados, and bananas",
        "Avoid alcohol, especially red wine, and processed foods",
        "Incorporate anti-inflammatory foods like berries and leafy greens",
        "Eat potassium-rich foods like sweet potatoes and cantaloupe",
        "Avoid skipping meals and maintain a steady blood sugar level"
    ]
    # ... (Other symptoms)
}

def generate_diet_plan(symptoms):
    diet_plan = {}
    for symptom in symptoms:
        if symptom in diet_recommendations:
            diet_plan[symptom] = diet_recommendations[symptom]
    return diet_plan

def format_diet_plan(diet_plan):
    formatted_plan = ""
    for symptom, recommendations in diet_plan.items():
        formatted_plan += f"### For {symptom}:\n"
        for recommendation in recommendations:
            formatted_plan += f"- {recommendation}\n"
        formatted_plan += "\n"
    return formatted_plan

class PDF(FPDF):
    def header(self):
        self.draw_border()
        self.set_font("Arial", "B", 16)
        self.set_text_color(255, 0, 0)
        self.cell(0, 10, "Mediquest - Your Health Companion", border=0, ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def draw_border(self):
        self.set_line_width(0.5)
        self.set_draw_color(0, 0, 0)
        self.rect(5, 5, self.w - 10, self.h - 10)

def generate_pdf(patient_name, patient_age, diet_plan):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 128, 0)
    pdf.cell(0, 10, "Patient Diet Plan", ln=True, align="C")
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(0, 10, f"Patient Age: {patient_age}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.date.today()}", ln=True)
    pdf.cell(0, 10, "-" * 40, ln=True)

    pdf.set_font("Arial", "", 10)
    for symptom, recommendations in diet_plan.items():
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 10, f"For {symptom}:", ln=True)
        pdf.set_text_color(0, 0, 0)
        for recommendation in recommendations:
            pdf.cell(0, 10, f" - {recommendation}", ln=True)
        pdf.cell(0, 10, "", ln=True)
        if pdf.get_y() > 250:
            pdf.add_page()

    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name

# App Configuration
st.set_page_config(
    page_title="Diet Plan Generator",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("MediQuest")
st.sidebar.markdown("### Features:")
st.sidebar.markdown("- 📝 **Personalized Diet Plans**")
st.sidebar.markdown("- 📄 **Downloadable PDFs**")
st.sidebar.markdown("- 💡 **Health Tips**")
st.sidebar.image(r"C:\Users\shara\OneDrive\Desktop\WhatsApp Image 2024-11-29 at 21.54.59_3918f1b5.jpg", caption="Your Health Companion")

st.sidebar.info("**Tip:** Select symptoms to get personalized dietary advice.")

# Header Section
st.title("🍎 Personalized Diet Plan Generator")
st.markdown("### Your companion for a healthier lifestyle")
st.image(r"C:\Users\shara\OneDrive\Desktop\WhatsApp Image 2024-11-29 at 22.27.48_d20f2435.jpg", use_column_width=True)

# Collecting patient details
with st.container():
    st.header("Patient Details")
    cols = st.columns(2)
    patient_name = cols[0].text_input("👤 Patient Name")
    patient_age = cols[1].number_input("🎂 Patient Age", min_value=1, max_value=120, step=1)

# Symptom Selection Section
st.header("Symptom Selection")
selected_symptoms = st.multiselect(
    "🩺 Select Symptoms:",
    list(diet_recommendations.keys()),
    help="Choose the symptoms to generate a tailored diet plan."
)

# Generate Diet Plan
if st.button("🔍 Generate Diet Plan"):
    if not patient_name:
        st.error("⚠️ Please enter the patient's name.")
    elif not patient_age:
        st.error("⚠️ Please enter the patient's age.")
    elif not selected_symptoms:
        st.error("⚠️ Please select at least one symptom to generate a diet plan.")
    else:
        with st.spinner("Generating your personalized diet plan..."):
            diet_plan = generate_diet_plan(selected_symptoms)
            formatted_plan = format_diet_plan(diet_plan)

            st.success("🎉 Diet Plan Generated Successfully!")
            st.markdown("### 📋 Your Personalized Diet Plan:")
            st.markdown(formatted_plan)

            pdf_file = generate_pdf(patient_name, patient_age, diet_plan)
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="💾 Download PDF",
                    data=file,
                    file_name="diet_plan.pdf",
                    mime="application/pdf"
                )
            st.balloons()
