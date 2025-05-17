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
    template='''
        Generate a detailed summary of cures and precautions for the plant disease: {disease}.
        Respond ONLY in the English language. Do not use any other language.

        Your response should follow this structure and provide specific, actionable, and well-researched insights:

        1. **Disease Name**
        - Full scientific and common name (if available)

        2. **Cause of the Disease**
        - Specify whether the cause is fungal, bacterial, viral, or due to environmental factors
        - Include specific pathogens or conditions (e.g., *Phytophthora infestans*, poor drainage)

        3. **Environmental Conditions Favoring the Disease**
        - Describe temperature, humidity, soil conditions, or season that promote the disease

        4. **Symptoms of the Disease**
        - Include early signs and progressive symptoms
        - Mention how symptoms appear on leaves, stems, roots, or fruits

        5. **Plants Commonly Affected**
        - List some examples of plant species or crops that are often affected

        6. **Treatment Methods**
        - Describe both **organic** (e.g., neem oil, compost tea) and **chemical** (e.g., fungicides, antibiotics) treatment options
        - Mention dosage, application frequency, and safety precautions

        7. **Preventive Measures**
        - Include crop rotation, soil treatment, spacing, irrigation practices, resistant plant varieties, etc.

        8. **Impact on Yield or Plant Health**
        - Explain how the disease affects productivity or quality of the crops if left untreated

        9. **Additional Recommendations**
        - Suggest monitoring strategies, agricultural best practices, or seasonal actions
        - Reference any tools, sensors, or technologies (e.g., moisture meters, AI-based disease detection)

        Be specific, concise, and factual. Avoid unnecessary filler content. Respond only in English.
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
        base_url = "http://127.0.0.1:8001"  # Update this with your actual server URL
        predicted_image_url = f"/static/predictions/{file.filename}"

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
        print(formatted_predictions)
        return JSONResponse(status_code=200, content=formatted_predictions)


    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"An error occurred while processing the image: {str(e)}"
        })

