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
model = YOLO("disease.pt")
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the request model for chat
class ChatRequest(BaseModel):
    question: str

# CHATBOT API Code Section
def get_agriculture_response(query: str):
    agriculture_keywords = ["farm", "farming", "agriculture", "crop", "plant", "soil", "harvest", "कृषि", "खेती", "बाली"]
    
    if any(keyword in query.lower() for keyword in agriculture_keywords):
        chat_prompt = PromptTemplate.from_template(
            '''You are an AI assistant specialized in agriculture and farming topics. 
            Provide a detailed and informative response to the following query about agriculture: {query}
            
            IMPORTANT: 
            - Respond ONLY in Nepali language.
            - Provide specific information related to the query.
            - If the query is general, give an overview of the topic.
            - Ensure your response is natural, conversational, and informative.'''
        )
    else:
        chat_prompt = PromptTemplate.from_template(
            '''You are an AI assistant specialized in agriculture and plant-related topics. 
            Analyze the following user input: {query}

            If the input is a greeting:
            Respond with a friendly greeting in Nepali and encourage the user to ask an agriculture-related question.

            If the input is not related to agriculture or plants:
            Politely explain in Nepali that you can only answer questions about agriculture and plants, 
            and encourage the user to ask an agriculture-related question.

            IMPORTANT: 
            - Always respond ONLY in Nepali language.
            - Ensure your response is natural and conversational.'''
        )
    
    llm = GoogleGenerativeAI(temperature=0.7, model="gemini-pro", api_key=apikey)
    chain = chat_prompt | llm
    response = chain.invoke({"query": query})
    return response

@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        question = request.question.strip()
        if not question:
            return JSONResponse(status_code=400, content={"error": "Bad Request! Please provide a valid question!"})

        response = get_agriculture_response(question)
        response_text = markdown.markdown(response)

        return JSONResponse(status_code=200, content={
            "question": question,
            "response": response_text
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": f"Sorry! Something went wrong: {str(e)}"
        })

# DISEASE DETECTION API Code Section
def generate_summary(disease: str):
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
            summary = generate_summary(disease)
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