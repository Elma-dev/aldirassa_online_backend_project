# Define the QuizContentAgent class
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from entities.quiz_entities import *

class QuizContentAgent():
    def __init__(self, model):
        self.__parser = PydanticOutputParser(pydantic_object=QuizContent)
        self.__model = model
        self.__system_prompt = '''
        You are an Arabic quiz generator based on the provided topics. Generate detailed questions for each topic.
        Follow these rules:
        1. Questions should be challenging but clear
        2. Each question must have 2-4 correct answers
        3. Options should be meaningful and relevant
        4. Questions should test understanding, not just memorization
        5. Content must be in Arabic

        {format_instructions}
        '''

        self.__user_prompt = '''
        Generate {num_questions} quiz questions for the module "{module_name}" in Arabic.
        Topics to cover: {topics}

        Requirements:
        - Questions should test different aspects of the topics
        - Include a mix of single and multiple correct answer questions
        - All content must be in Arabic
        - Ensure correct answers are clearly marked
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
        try:
            # Validate inputs
            if not quiz_input.topics:
                raise ValueError("No topics provided for quiz generation")

            content = self.chain.invoke(
                {
                    'module_name': quiz_input.module_name,
                    'course_name': quiz_input.course_name,
                    'topics': ', '.join(quiz_input.topics),
                    'num_questions': num_questions
                }
            )

            # Validate generated content
            if not content or not content.questions:
                raise ValueError("Failed to generate valid quiz content")

            return content

        except Exception as e:
            print(f"Error in quiz generation: {str(e)}")
            raise
