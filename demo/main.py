import streamlit as st
from ultralytics import YOLO
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
import os, markdown
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# API key for the Google API
apikey = os.getenv("API_KEY")

# Initialize YOLO model
model = YOLO("best.pt")

# Setup upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def generate_summary(disease):
    summary_template = PromptTemplate(
        input_variables=['disease'],
        template='''Generate a summary of cures and precautions for the plant disease: {disease}. 
        Include treatment methods and preventive measures. 
        IMPORTANT: Respond ONLY in Nepali language. Do not use any English.
        
        Your response should follow this structure in Nepali:
        1. रोगको नाम (Disease Name)
        2. रोगको कारण (Cause of the Disease)
        3. रोगको लक्षणहरू (Symptoms of the Disease)
        4. उपचार विधिहरू (Treatment Methods)
        5. रोकथामका उपायहरू (Preventive Measures)
        6. थप सुझावहरू (Additional Recommendations)
        '''
    )
    llm = GoogleGenerativeAI(temperature=0.7, model="gemini-pro", api_key=apikey)
    summary_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True)
    summary = summary_chain.run(disease=disease)
    return markdown.markdown(summary)

# Streamlit UI
st.set_page_config(layout="wide")  # Use wide layout

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .main-header {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subtitle {
        color: #9E9E9E;
        font-size: 1.2rem;
    }
    .upload-section {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* Hide Streamlit's default elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown("""
    <div class='main-header'>
        <div class='title'>
            <img src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzRDQUY1MCI+PHBhdGggZD0iTTYuNTggNkM0LjM3IDYgMi4yNSA3LjE3IDIuMjUgOS41YzAgMS4yNy42NSAyLjI4IDEuNjQgMi45MXYuMzhjMCAyLjcgMi41NiA0LjcxIDUuMzYgNC43MXYzYzQuMTctMi4yOSA2LjUtNC43NyA2LjUtOC4yOVY5LjRjMS4yLS41MiAyLTEuNTcgMi0yLjkgMC0yLjMzLTIuMTItMy41LTQuMzMtMy41LTEuMTYgMC0yLjIyLjMxLTMuMTYuOTFDOS4yMyA2LjU3IDcuOTIgNiA2LjU4IDZ6Ii8+PC9zdmc+' style='width: 40px; height: 40px;' />
            Tea Leaf Disease Detection
        </div>
        <div class='subtitle'>Upload an image to detect tea leaf diseases using AI</div>
    </div>
""", unsafe_allow_html=True)

# Create three columns for better spacing
left_col, center_col, right_col = st.columns([1, 2, 1])

with center_col:
    uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Save the uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Create two columns for image and results
    col_img, col_results = st.columns([1, 1])
    
    with col_img:
        st.markdown("""
            <div style='
                background-color: #1E1E1E;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            '>
                <h3 style='color: white; margin-bottom: 15px;'>Uploaded Image</h3>
            </div>
        """, unsafe_allow_html=True)
        st.image(filepath, use_column_width=True)
    
    with col_results:
        st.markdown("""
            <div style='
                background-color: #1E1E1E;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            '>
                <h3 style='color: white; margin-bottom: 15px;'>Detection Results</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Add results content
        with st.spinner("Analyzing image..."):
            results = model(source=filepath, save=True)
            predictions = results[0].boxes.data.tolist()
            class_names = results[0].names
            
            if len(predictions) > 0:
                for pred in predictions:
                    class_id = int(pred[5])
                    confidence = float(pred[4])
                    disease = class_names[class_id]
                    
                    # Result card
                    st.markdown(f"""
                        <div style='
                            background-color: #2E2E2E;
                            padding: 20px;
                            border-radius: 10px;
                            margin-bottom: 15px;
                            border: 1px solid #3E3E3E;
                        '>
                            <div style='
                                display: flex;
                                align-items: center;
                                margin-bottom: 10px;
                            '>
                                <span style='
                                    background-color: #4CAF50;
                                    padding: 5px 10px;
                                    border-radius: 5px;
                                    color: white;
                                    font-weight: bold;
                                    margin-right: 10px;
                                '>🔍 Detected</span>
                                <span style='color: white; font-size: 16px;'>{disease}</span>
                            </div>
                            <div style='
                                color: #9E9E9E;
                                margin-top: 10px;
                            '>
                                Confidence Score: <span style='color: #4CAF50; font-weight: bold;'>{confidence:.1%}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Detailed analysis expander
                    with st.expander("📋 See Detailed Analysis in Nepali"):
                        summary = generate_summary(disease)
                        st.markdown(f"""
                            <div style='
                                background-color: #2E2E2E;
                                padding: 20px;
                                border-radius: 10px;
                                color: white;
                            '>
                                {summary}
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("❌ No disease detected in the image")

        # Clear button
        if st.button("🔄 Clear and Upload Another Image"):
            st.experimental_rerun()