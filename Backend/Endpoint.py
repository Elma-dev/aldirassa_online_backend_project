from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from Chatbot import ChatTopicAgent, TopicContent, TopicInput,Topic
import os
from dotenv import load_dotenv

load_dotenv()

topics = ['Understanding Data Types', 'Handling Missing Values', 'Data Normalization and Standardization']

app = FastAPI()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize the ChatTopicAgent
agent = ChatTopicAgent(topics, openai_api_key)

# Pydantic model for request body
class QuestionRequest(BaseModel):
    question: str

# POST endpoint to ask a question
@app.post("/ask")
async def ask_question(request: QuestionRequest) -> Dict[str, str]:
    try:
        response = agent.ask_question(request.question)
        return response
    except Exception as e:
        return {
            "error": f"An error occurred: {str(e)}",
            "answer": "Could not generate answer",
            "sources": [],
        }

# Optional: GET endpoint for testing
@app.get("/")
async def root():
    return {"message": "Welcome to the Q/A Agent API!"}