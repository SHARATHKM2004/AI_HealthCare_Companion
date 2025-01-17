# Advanced Doctor's Assistant Dashboard
##App link-> https://aihealthcarecompanion-a8m4gvvm6vxs8r2mgsn5uy.streamlit.app/

The Advanced Doctor's Assistant Dashboard is an interactive Streamlit application designed for comprehensive medical symptom tracking, medical image analysis, and detailed reporting. It leverages advanced technologies such as the Falcon 180B model for medical guidance and integrates machine learning models for analyzing medical images.

## Features

### Symptom Tracker
- **Symptom Analysis**:
  - Users can input detailed symptoms related to respiratory, digestive, and general health.
  - The system provides medical advice based on the symptoms entered.
- **PDF Report Generation**:
  - The application generates a downloadable PDF report that includes:
    - Patient data
    - Detailed symptom information
    - Analysis results
    - Pain management advice
    - Preventive measures

### Medical Image Analysis
- **Image Upload and Analysis**:
  - Users can upload medical images (e.g., X-rays) for analysis.
  - The system identifies potential conditions such as lung cancer, pneumonia, and COVID-19 from the images.
- **Visualization**:
  - The results of the analysis are visualized with:
    - Diagnosis
    - Detailed findings
    - Recommendations
    - Severity assessment

### Reports & Visualizations
- **Symptom Trends**:
  - Interactive charts and graphs display trends in symptoms and pain levels over time.
- **Symptom Distribution**:
  - Pie charts illustrate the distribution of reported symptoms.

## Installation

To set up the application, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/rabiyajeh/Falcon-Hackathon-Healthcare-app.git
   cd Falcon-Hackathon-Healthcare-app
2. **Create virtual Environment**
    `python -m venv venv
     source venv/bin/activate  # On Windows, use venv\Scripts\activate`

3. **Install Required Python Packages**
   `pip install -r requirements.txt`

4.  **Run the Application**
    `streamlit run Home.py`

5.  **Open your browser and navigate to**
      `http://localhost:8501`

### Usage
- Upon running the application, you will be presented with the Advanced Doctor's Assistant Dashboard interface.
- Input symptoms or upload medical images to initiate analysis.
- Explore generated reports, visualizations, and recommendations based on the entered data.



