from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Type , Dict , Union
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.schema import Document
from enum import Enum
import json
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

model = ChatOpenAI(model_name="gpt-4o-mini")

class Topic(BaseModel):
  topic_name:str=Field(description='Topic Name')
  explanation:str=Field(description='Detailed Explanation of the Topic')

class TopicContent(BaseModel):
  module_name:str=Field(description='Module Name')
  introduction:str=Field(description='Brief Introduction to the Module')
  topics:List[Topic]

class TopicInput():
  module_name:str
  course_name:str
  topics:List[str]


class ChatTopicAgent:
    def __init__(self, topics_list, openai_api_key):
        self.topics_list = topics_list
        os.environ["OPENAI_API_KEY"] = openai_api_key

        # Initialize components
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.embeddings = OpenAIEmbeddings()

        # Create documents from topics list
        documents = self._create_documents()

        # Create vector store
        self.vector_store = InMemoryVectorStore.from_documents(
            self.text_splitter.split_documents(documents),
            self.embeddings
        )
        self.llm = model

        self.qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}
            )
        )

    def _create_documents(self):
        documents = []
        for topic in self.topics_list:
            # Assuming each topic has 'introduction' and 'module_name'
            documents.append(Document(
                page_content=topic.explanation,
                metadata={"source": topic.topic_name}
            ))
        return documents

    def ask_question(self, question: str) -> dict:
        """Ask a question and return response with RAG details"""
        try:
            result = self.qa_chain({"question": question})

            return {
                "answer": result["answer"],
                "sources": result["sources"],
            }
        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "answer": "Could not generate answer",
                "sources": [],
            }

topics = [Topic(topic_name='Understanding Data Types', explanation='In machine learning, data comes in various forms, known as data types. The most common data types include numerical (which can be further divided into continuous and discrete), categorical (which can be nominal or ordinal), and text data. Understanding these types is important because they determine how we can manipulate and analyze the data. For example, numerical data can be used for mathematical operations, while categorical data often requires encoding techniques to convert it into a numerical format for analysis.'),
 Topic(topic_name='Handling Missing Values', explanation='Missing values are common in datasets and can lead to biased or inaccurate models if not addressed properly. There are several strategies to handle missing values, such as removing rows with missing data, filling in missing values using techniques like mean, median, or mode imputation, or predicting them using models. Choosing the right method depends on the nature of the data and the importance of the missing values in the analysis.'),
 Topic(topic_name='Data Normalization and Standardization', explanation="Normalization and standardization are techniques used to scale numerical data, ensuring that different features contribute equally to the analysis. Normalization typically rescales the data to a range between 0 and 1, while standardization transforms the data to have a mean of 0 and a standard deviation of 1. This is particularly important for algorithms that rely on distance calculations, such as k-nearest neighbors and gradient descent, as it helps improve the model's performance and convergence speed.")]

# Define FastAPI app
app = FastAPI()

# Input data model
class QuestionRequest(BaseModel):
    question: str

# Response model
class SimpleResponse(BaseModel):
    response: str
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the agent
agent = ChatTopicAgent(topics, openai_api_key)

# Endpoint to handle questions
@app.post("/ask", response_model=SimpleResponse)
async def ask_question(request: QuestionRequest):
    """Endpoint to ask a question and return a simple text response."""
    try:
        result = agent.ask_question(request.question)
        if "error" in result:
            raise ValueError(result["error"])
        return SimpleResponse(response=result["answer"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
