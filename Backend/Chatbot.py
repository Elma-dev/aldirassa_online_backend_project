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

model = ChatOpenAI(model_name="gpt.4o-mini")

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