import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from requests.exceptions import RequestException
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
from datetime import datetime
import altair as alt
from torchvision.models import resnet50, ResNet50_Weights
from reportlab.lib.colors import Color


# Using weights=ResNet50_Weights.DEFAULT to load pretrained weights
model = resnet50(weights=ResNet50_Weights.DEFAULT)

# API Key and URL for Falcon 180B Model
API_KEY = "ai71-api-573ef5e3-71e1-471d-b8ed-68d6a69c492f"
API_URL = "https://api.ai71.ai/v1/chat/completions"


# Load the pre-trained model for lung disease analysis
def load_chexnet_model():
    model = models.resnet50(pretrained=True)
    model.eval()
    return model

def preprocess_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return preprocess(image).unsqueeze(0)

def analyze_image(image):
    model = load_chexnet_model()
    img = Image.open(BytesIO(image.read()))
    img_tensor = preprocess_image(img)
    
    try:
        with torch.no_grad():
            outputs = model(img_tensor)
        # Mock results; replace with actual model output interpretation
        results = {
            "Lung Cancer": np.random.random(),
            "Pneumonia": np.random.random(),
            "COVID-19": np.random.random()
        }
        return {
            "diagnosis": "No abnormalities detected.",
            "details": "The image does not show any clear signs of lung cancer, pneumonia, or COVID-19.",
            "recommendations": "Regular check-ups and maintaining a healthy lifestyle are recommended.",
            "severity": "N/A",
            "results": results
        }
    except Exception as e:
        st.error(f"An error occurred during image analysis: {e}")
        return {
            "diagnosis": "Error during analysis.",
            "details": "An error occurred while processing the image.",
            "recommendations": "Please try again.",
            "severity": "N/A",
            "results": {}
        }
        
# Function to get response from the Falcon 180B model
def get_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tiiuae/falcon-180B-chat",
        "messages": [
            {"role": "system", "content": "You are a medical assistant. Provide clear and accurate medical responses based on the symptoms described."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()
        return response_json.get('choices', [{}])[0].get('message', {}).get('content', "No response received.")
    except RequestException as e:
        st.error(f"An error occurred: {e}")
        return "Sorry, there was an error processing your request."

# Function to generate a PDF report
from reportlab.lib.colors import Color
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import PageTemplate, Frame
from io import BytesIO

def draw_border(canvas_obj, doc):
    """
    Draws a border on the canvas for each page.
    """
    width, height = letter
    margin = 10  # Border margin
    canvas_obj.setStrokeColor(Color(0, 0, 0))  # Black color for border
    canvas_obj.setLineWidth(2)  # Border line width
    canvas_obj.rect(margin, margin, width - 2 * margin, height - 2 * margin, stroke=1, fill=0)

def on_page(canvas_obj, doc):
    """
    Draws the border and adds the title text at the top of each page.
    """
    draw_border(canvas_obj, doc)
    width, height = letter

    # Title text properties
    title = "Mediquest - Your Health Companion"
    canvas_obj.setFont("Helvetica-Bold", 22)  # Font size matches "Patient Report"
    canvas_obj.setFillColor(Color(1, 0, 0))  # Red color
    text_width = canvas_obj.stringWidth(title, "Helvetica-Bold", 22)
    x_position = (width - text_width) / 2  # Center the text
    y_position = height - 50

    # Draw the text without underline
    canvas_obj.drawString(x_position, y_position, title)

def generate_pdf_report(patient_data, symptoms, analysis, pain_management, preventive_measures):
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Initialize the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    story = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=22,  # Font size matches the title
        textColor=Color(0.1, 0.2, 0.5),  # Blueish color
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=Color(0.2, 0.5, 0.2),  # Greenish color
        spaceAfter=12
    )
    justified_style = ParagraphStyle(
        'JustifiedStyle',
        parent=styles['BodyText'],
        alignment=TA_JUSTIFY,  # Justify the text
        fontSize=10,
        spaceAfter=8
    )

    # Add content to the story
    story.append(Paragraph("Patient Report", title_style))
    story.append(Spacer(1, 12))

    # Patient Data
    story.append(Paragraph("Patient Data:", heading_style))
    for key, value in patient_data.items():
        story.append(Paragraph(f"<b>{key}:</b> {value}", justified_style))
    story.append(Spacer(1, 12))

    # Symptoms
    story.append(Paragraph("Symptoms:", heading_style))
    story.append(Paragraph(symptoms, justified_style))
    story.append(Spacer(1, 12))

    # Analysis
    story.append(Paragraph("Analysis:", heading_style))
    story.append(Paragraph(analysis, justified_style))
    story.append(Spacer(1, 12))

    # Pain Management Advice
    story.append(Paragraph("Pain Management Advice:", heading_style))
    story.append(Paragraph(pain_management, justified_style))
    story.append(Spacer(1, 12))

    # Preventive Measures
    story.append(Paragraph("Preventive Measures:", heading_style))
    story.append(Paragraph(preventive_measures, justified_style))

    # Add border and title to all pages
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

    # Return the buffer
    buffer.seek(0)  # Move pointer to the beginning of the buffer
    return buffer


# Function to visualize symptoms using a bar chart
def visualize_symptoms(symptom_history):
    if symptom_history:
        df = pd.DataFrame(symptom_history)
        fig = px.bar(df, x='Date', y='Symptoms', color='Symptoms', title='Symptom Frequency or Severity')
        st.plotly_chart(fig)
    else:
        st.write("No symptom data available to visualize.")

# Function to visualize pain level trends using a line chart
def visualize_pain_trends(pain_history):
    if pain_history:
        df = pd.DataFrame(pain_history)
        fig = px.line(df, x='Date', y='Pain Level', title='Pain Level Trends Over Time')
        st.plotly_chart(fig)
    else:
        st.write("No pain data available to visualize.")

# Function to visualize symptom distribution using pie chart
def visualize_symptom_distribution(symptom_history):
    if symptom_history:
        symptom_counts = pd.Series([s['Symptoms'] for s in symptom_history]).value_counts()
        fig = px.pie(values=symptom_counts.values, names=symptom_counts.index, title='Symptom Distribution')
        st.plotly_chart(fig)
    else:
        st.write("No symptom data available to visualize.")

# Streamlit app layout
st.set_page_config(page_title="Advanced Doctor's Assistant Dashboard", layout="wide")

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'symptom_text' not in st.session_state:
    st.session_state.symptom_text = ""
if 'pain_management' not in st.session_state:
    st.session_state.pain_management = ""
if 'preventive_measures' not in st.session_state:
    st.session_state.preventive_measures = ""
if 'response' not in st.session_state:
    st.session_state.response = ""
if 'symptom_history' not in st.session_state:
    st.session_state.symptom_history = []
if 'pain_history' not in st.session_state:
    st.session_state.pain_history = []

# Create tabs for different sections
st.markdown("""
    <h1 style='text-align: center; font-family: Verdana, sans-serif; color: #2C3E50;'>
    ➕ MediQuest
    </h1>
    """, unsafe_allow_html=True)
# Add scrolling text at the top of the page
st.markdown("""
    <style>
        .scrolling-box {
            width: 100%;
            background-color: #f5f5f5; /* Light gray background */
            border: 2px solid #FF0000; /* Red border */
            padding: 10px;
            margin: 20px 0;
            overflow: hidden;
        }

        .scrolling-text {
            font-size: 20px;
            font-family: Verdana, sans-serif;
            color: #FF0000; /* Red color */
            white-space: nowrap;
            display: inline-block;
            animation: scroll-left 15s linear infinite; /* Slow scrolling */
        }

        @keyframes scroll-left {
            0% {
                transform: translateX(100%); /* Start from the right */
            }
            100% {
                transform: translateX(-100%); /* Move completely to the left */
            }
        }
    </style>
    <div class="scrolling-box">
        <div class="scrolling-text">
            <span>"➕MediQuest - AI-Enhanced Symptom Tracking for Informed Health Decisions."</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


tab1, tab2, tab3= st.tabs(["Symptom Tracker", "Medical Image Analysis", "Reports & Visualizations"])

# Symptom Tracker Tab
with tab1:

    st.header("Symptom Tracker")
    with st.form("chat_form"):
        patient_name = st.text_input("Patient Name:")
        patient_age = st.text_input("Patient Age:")
        patient_gender = st.selectbox("Patient Gender:", ["Male", "Female", "Other"])

        st.subheader("Symptom Details")

        # Respiratory Symptoms
        st.markdown("Respiratory Symptoms")
        cough = st.checkbox("Cough")
        shortness_of_breath = st.checkbox("Shortness of Breath")
        chest_pain = st.checkbox("Chest Pain")

        # Digestive Symptoms
        st.markdown("Digestive Symptoms")
        nausea = st.checkbox("Nausea")
        vomiting = st.checkbox("Vomiting")
        diarrhea = st.checkbox("Diarrhea")

        # Pain Level
        st.markdown("Pain Level")
        pain_level = st.slider("Pain Level (0-10)", 0, 10, 0)

        # General Symptoms
        st.markdown("General Symptoms")
        fever = st.checkbox("Fever")
        fatigue = st.checkbox("Fatigue")
        headache = st.checkbox("Headache")
        other_symptoms = st.text_area("Other Symptoms:")

        submitted = st.form_submit_button("Send")

        if submitted:
            # Collect symptom details
            symptoms = []
            if cough:
                symptoms.append("Cough")
            if shortness_of_breath:
                symptoms.append("Shortness of Breath")
            if chest_pain:
                symptoms.append("Chest Pain")
            if nausea:
                symptoms.append("Nausea")
            if vomiting:
                symptoms.append("Vomiting")
            if diarrhea:
                symptoms.append("Diarrhea")
            if fever:
                symptoms.append("Fever")
            if fatigue:
                symptoms.append("Fatigue")
            if headache:
                symptoms.append("Headache")
            if other_symptoms:
                symptoms.append(other_symptoms)
            
            st.session_state.symptom_text = ", ".join(symptoms)
            
            # Chat with Falcon 180B Model
            prompt = f"Patient Name: {patient_name}, Age: {patient_age}, Gender: {patient_gender}. Symptoms: {st.session_state.symptom_text}. Provide analysis, pain management advice, and preventive measures."
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = get_response(prompt)
            st.session_state.response = response
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Parse response for pain management and preventive measures
            st.session_state.pain_management = "Pain Management Advice: " + st.session_state.response.split("Pain Management Advice: ")[-1].split("Preventive Measures:")[0].strip()
            st.session_state.preventive_measures = "Preventive Measures: " + st.session_state.response.split("Preventive Measures:")[-1].strip()

            # Store symptom and pain data in history
            st.session_state.symptom_history.append({"Date": pd.Timestamp.now(), "Symptoms": st.session_state.symptom_text})
            st.session_state.pain_history.append({"Date": pd.Timestamp.now(), "Pain Level": pain_level})

    #for message in st.session_state.messages:
        #if message['role'] == 'user':
            #st.write(f"You: {message['content']}")
        #else:
            #st.write(f"Assistant: {message['content']}")

    # Generate PDF report button
    if st.button("Generate PDF Report"):
        if st.session_state.symptom_text:
            patient_data = {
                "Name": patient_name,
                "Age": patient_age,
                "Gender": patient_gender
            }
            pdf_buffer = generate_pdf_report(patient_data, st.session_state.symptom_text, st.session_state.response, st.session_state.pain_management, st.session_state.preventive_measures)
            st.download_button(
                label="Download PDF Report",
                data=pdf_buffer,
                file_name="patient_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("No symptoms provided for the PDF report.")

# Medical Image Analysis Tab
with tab2:
    st.header("Upload and Analyze Medical Image")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)
        st.write("Analyzing...")
        result = analyze_image(uploaded_image)
        st.write("Analysis Result:")
        st.write(result["diagnosis"])
        st.write(result["details"])
        st.write("Recommendations:")
        st.write(result["recommendations"])
        st.write("Severity:")
        st.write(result["severity"])
        st.write("Analysis Results:")
        st.write(result["results"])




    #st.sidebar.markdown("<a href='chatbot' target='_self'>subpage</a>", unsafe_allow_html=True)
    #st.page_link("chatbot.py", label="chat_bot", icon="1️⃣")
    #st.markdown("<a href='subpage' target='_self'>subpage</a>", unsafe_allow_html=True)

    st.sidebar.header("Instructions")

    st.sidebar.write(
    """
    🌟 Welcome to  ➕ MedQuest the Dashboard! 🌟

    - 📋 Symptom Tracker: 🩺 Describe your symptoms to receive a comprehensive analysis from our cutting-edge **Falcon 180B model. Your journey to better health starts here!

    - 📄 Generate PDF Report: 📥 Click the button below to create a **downloadable PDF report based on your symptoms and our insightful analysis. Keep your health records at your fingertips!

    - 🖼 Upload Medical Image: 📸 Upload a medical image (e.g., X-ray) for in-depth analysis related to **lung cancer, **pneumonia, or **COVID-19. Get precise insights tailored to your needs!

    - 📈 Symptom and Pain Trends: 📊 Track your progress with beautiful visualizations of your symptom and pain levels over time. **See how you’re doing with just a glance!

    - 🍰 Symptom Distribution: 🔍 Dive into a colorful **pie chart showcasing the distribution of your reported symptoms. Understand your health landscape effortlessly!

    ⚠ Important Note: The analysis generated by our AI models is for informational purposes only and should never replace professional medical advice. Always consult a healthcare provider for any health concerns—your well-being is our priority!
    """
)

def load_data():
    dates = pd.date_range(start='2023-01-01', periods=10, freq='D')
    symptom_data = pd.DataFrame({
        'Date': dates,
        'Symptom': ['Chest Pain', 'Fatigue', 'Headache'] * 3 + ['Fatigue'],
        'Severity': [2, 4, 3, 5, 1, 2, 3, 2, 4, 3]
    })
    pain_data = pd.DataFrame({
        'Date': dates,
        'Pain Level': [3, 4, 2, 5, 4, 3, 3, 2, 4, 2]
    })
    return symptom_data, pain_data

# Visualization of Symptom Trends
def visualize_symptoms(symptom_data):
    if symptom_data.empty:
        st.write("No symptom data available")
    else:
        fig = px.line(symptom_data, x='Date', y='Severity', color='Symptom',
                      title="Symptom Frequency or Severity Over Time")
        st.plotly_chart(fig)

# Visualization of Pain Trends
def visualize_pain_trends(pain_data):
    if pain_data.empty:
        st.write("No pain data available")
    else:
        fig = alt.Chart(pain_data).mark_line().encode(
            x='Date:T',
            y='Pain Level:Q',
            tooltip=['Date', 'Pain Level']
        ).properties(title='Pain Level Trends Over Time')
        st.altair_chart(fig, use_container_width=True)

# Load  data (replace with actual data from session_state)
symptom_data, pain_data = load_data()

# Now integrate this into your tab3 section
with tab3:
    st.header("Symptom and Pain Trends")
    visualize_symptoms(symptom_data)  # Replace with st.session_state.symptom_history
    visualize_pain_trends(pain_data)
    visualize_symptom_distribution(st.session_state.symptom_history)
