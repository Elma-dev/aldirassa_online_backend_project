from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import json
import os
import getpass
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from openai import OpenAI
#import nest_asyncio

### key
import os
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Now you can use the openai_api_key in your code
if openai_api_key:
    print(f"OpenAI API Key loaded")
else:
    print("OpenAI API Key not found!")


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Define the models for the quiz question and content
class QuizQuestion(BaseModel):
    question: str = Field(description='The quiz question')
    options: List[str] = Field(description='List of multiple-choice options')
    correct_answers: List[str] = Field(description='List of correct answers (can have multiple)')

class QuizContent(BaseModel):
    module_name: str = Field(description='Module Name')
    questions: List[QuizQuestion] = Field(description='List of quiz questions')

# Define the quiz input model without num_questions
class QuizInput(BaseModel):
    module_name: str
    course_name: str
    topics: List[str]

# Define the QuizContentAgent class
class QuizContentAgent():
    def __init__(self, model):
        self.__parser = PydanticOutputParser(pydantic_object=QuizContent)
        self.__model = model
        self.__system_prompt = '''
        You are a quiz generator based on the topics provided. For each topic, create a set of {num_questions} quiz questions with multiple-choice options.
        The output should contain {num_questions} questions for each topic along with their options and the correct answers. Ensure each question has at least one correct answer and that all answers are included.

        ### Input Data
        1. **Module Name**: [Module Name]
        2. **Topics**: [List of Topics]
        3. **Number of Questions**: [num_questions]

        {format_instructions}

        ### Expected Output:
        The result should be a JSON object that contains the following keys:
        - "module_name": The module's name.
        - "questions": An array of {num_questions} question objects. Each question should have:
            - "question": The question text.
            - "options": An array of multiple-choice options.
            - "correct_answers": An array of correct answers (Its very very important to have at least one correct answer).

        Ensure the JSON is valid and complete. Do not include any extra text.
        '''

        self.__user_prompt = '''
        Generate {num_questions} quiz questions for the module {module_name} in the course "{course_name}".
        The module includes the following topics: {topics}.
        Please provide {num_questions} questions for each topic with multiple-choice options. Some questions may have more than one correct answer, so list all correct answers accordingly.

        The output should be a valid JSON object with the following fields:
        - "module_name": The module's name.
        - "questions": An array of {num_questions} questions, each having:
            - "question": The question text.
            - "options": Multiple-choice options.
            - "correct_answers": A list of correct answers for each question.
        '''

        self.__template = ChatPromptTemplate(
            [
                ('system', self.__system_prompt),
                ('human', self.__user_prompt)
            ],
            input=['module_name', 'course_name', 'topics', 'num_questions'],
            partial_variables={"format_instructions": self.__parser.get_format_instructions()}
        )

        self.chain = self.__template | self.__model | self.__parser

    def generate_quiz_content(self, quiz_input: QuizInput, num_questions: int) -> QuizContent:
        content = self.chain.invoke(
            {
                'module_name': quiz_input.module_name,
                'course_name': quiz_input.course_name,
                'topics': ', '.join(quiz_input.topics),
                'num_questions': num_questions * len(quiz_input.topics)
            }
        )
        return content

# Instantiate the agent with a model
quiz_content_agent = QuizContentAgent(model=model)

# Create FastAPI app
app = FastAPI()

@app.post("/generate_quiz/")
async def generate_quiz(quiz_inputs: List[QuizInput]):
    items = []
    for quiz_input in quiz_inputs:
        try:
            quiz_content = quiz_content_agent.generate_quiz_content(quiz_input, 5)
            items.append(quiz_content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"quiz_contents": items}

# Apply nest_asyncio to allow nested event loops
#nest_asyncio.apply()
import uvicorn
# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)