
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from Chatbot import ChatTopicAgent, TopicContent,Topic
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="/aldirassa_online_backend_project/Frontend"), name="static")

# Serve the main frontend file
@app.get("/")
async def read_index():
    return FileResponse("/aldirassa_online_backend_project/Frontend/index.html")

# Initialize ChatTopicAgent
topics_list = [Topic(topic_name='Understanding Data Types', explanation='In machine learning, data comes in various forms, known as data types. The most common data types include numerical (which can be further divided into continuous and discrete), categorical (which can be nominal or ordinal), and text data. Understanding these types is important because they determine how we can manipulate and analyze the data. For example, numerical data can be used for mathematical operations, while categorical data often requires encoding techniques to convert it into a numerical format for analysis.'),
 Topic(topic_name='Handling Missing Values', explanation='Missing values are common in datasets and can lead to biased or inaccurate models if not addressed properly. There are several strategies to handle missing values, such as removing rows with missing data, filling in missing values using techniques like mean, median, or mode imputation, or predicting them using models. Choosing the right method depends on the nature of the data and the importance of the missing values in the analysis.'),
 Topic(topic_name='Data Normalization and Standardization', explanation="Normalization and standardization are techniques used to scale numerical data, ensuring that different features contribute equally to the analysis. Normalization typically rescales the data to a range between 0 and 1, while standardization transforms the data to have a mean of 0 and a standard deviation of 1. This is particularly important for algorithms that rely on distance calculations, such as k-nearest neighbors and gradient descent, as it helps improve the model's performance and convergence speed.")]

chat_agent = ChatTopicAgent(topics_list, os.getenv("OPENAI_API_KEY"))

# Define API endpoint for asking questions
@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        return JSONResponse(status_code=400, content={"error": "Question is required"})
    
    response = chat_agent.ask_question(question)
    return JSONResponse(content=response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)