from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles  # Import StaticFiles
from ultralytics import YOLO
import os, markdown
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from urllib.parse import urljoin

# Load environment variables
load_dotenv()

# API key for the Google API
apikey = os.getenv("API_KEY")

app = FastAPI()

# Mount the static directory so FastAPI can serve static files

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
model = YOLO("best.pt")

# Define directories for uploads and predictions
UPLOAD_FOLDER = 'static/uploads'
PREDICTED_FOLDER = 'static'

# Create folders if they do not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICTED_FOLDER, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
def generate_summary(disease: str):
    summary_template = PromptTemplate(
        input_variables=['disease'],
        template='''Generate a summary of cures and precautions for the plant disease: {disease}. 
        Include treatment methods and preventive measures. 
        IMPORTANT: Respond ONLY in English language. Do not use any Other Language.

        Your response should follow this structure:
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

        # Run YOLO model prediction with explicit save path
        results = model.predict(
            source=filepath,
            save=True,
            conf=0.5,
            project=PREDICTED_FOLDER,  # Specify the project directory
            name='predictions',  # Specify a name for the run
            exist_ok=True  # Overwrite existing files
        )
        

        # Construct the full URL for the predicted image
        # base_url = "http://172.25.98.96:8000"  # Update this with your actual server URL
        base_url = "http://192.168.18.10:8000"  # Update this with your actual server URL
        predicted_image_url = urljoin(base_url, f"/static/predictions/{file.filename}")

        # Get predictions and disease summaries
        predictions = results[0].boxes.data.tolist()
        class_names = results[0].names

        # Format the predictions with summaries
        formatted_predictions = []
        for pred in predictions:
            class_id = int(pred[5])
            confidence = float(pred[4])
            disease = class_names[class_id]
            summary = generate_summary(disease)
            formatted_predictions.append({
                'class': disease,
                'summary': summary,
                'confidence': confidence,
                'predicted_image': predicted_image_url
            })

         # If no predictions
        if len(formatted_predictions) == 0:
            return JSONResponse(status_code=200, content={ "message": "No disease detected"})

        return JSONResponse(status_code=200, content=formatted_predictions)


    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"An error occurred while processing the image: {str(e)}"
        })

