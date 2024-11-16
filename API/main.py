# Importing the Necessary Libraries
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ultralytics import YOLO
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from fastapi.responses import JSONResponse
import os, markdown
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# API key for the Google API
apikey = os.getenv("API_KEY")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the YOLO model
model = YOLO("best.pt")
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# DISEASE DETECTION API Code Section
def generate_summary(disease: str):
    summary_template = PromptTemplate(
        input_variables=['disease'],
        template='''Generate a summary of cures and precautions for the plant disease: {disease}. 
        Include treatment methods and preventive measures. 
        IMPORTANT: Respond ONLY in English language. Do not use any Other Language.
        
        Your response should follow this structure in Nepali:
        1. Disease Name
        2. Cause of the Disease
        3. Symptoms of the Disease
        4. Treatment Methods
        5. Preventive Measures
        6. Additional Recommendations
        '''
    )
    llm = GoogleGenerativeAI(temperature=0.7, model="gemini-1.5-flash", api_key=apikey)
    summary_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True)
    summary = summary_chain.run(disease=disease)
    return markdown.markdown(summary)

@app.post("/predict/")
async def predict_disease(file: UploadFile = File(...)):
    try:
        if not file:
            return JSONResponse(status_code=400, content={"error": "No file uploaded"})

        # Save the uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(filepath, "wb") as f:
            f.write(await file.read())

        # Run YOLO model prediction
        results = model(source=filepath, save=True, conf=0.4)

        predictions = results[0].boxes.data.tolist()
        class_names = results[0].names

        # Format the predictions
        formatted_predictions = []
        for pred in predictions:
            class_id = int(pred[5])
            confidence = pred[4]
            disease = class_names[class_id]
            # summary = generate_summary(disease)
            summary = f"Summary for {disease} is not available"
            formatted_predictions.append({
                'class': disease,
                'summary': summary,
                'confidence': confidence
            })
        # If no predictions
        if len(formatted_predictions) == 0:
            return JSONResponse(status_code=200, content={ "message": "No disease detected"})

        return JSONResponse(status_code=200, content=formatted_predictions)

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": f"Sorry! Something went wrong: {str(e)}"
        })