from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from agents.agent_chek_relevence import *
from utils.check_model_status import *
from agents.skills_assessment_agent import *
from agents.skills_assessement_evaluator_agent import *
from agents.topic_content_agent import *
from entities.skills_entities import *
from entities.learning_path_entities import *
from entities.topic_content_entities import *
from agents.learning_path_agent import *
from agents.resource_recommendation_agent import *
from agents.qa_topic_agent import *
from entities.qa_entities import *
from agents.exercice_agent import *
from entities.exercice_agent_entities import *
from agents.quiz_agent import *
from entities.quiz_entities import *
from utils.quiz_correction_utils import *
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
model = get_model("gpt-4o-mini")
app.mount("/assets", StaticFiles(directory="../Frontend/assets"), name="assets")
app.mount("/media", StaticFiles(directory="../Frontend/assets/media"), name="media")


@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("../Frontend/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)
    
@app.get("/evaluation", response_class=HTMLResponse)
async def read_evaluation():
    with open("../Frontend/evaluation.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)
    
@app.get("/learningpath", response_class=HTMLResponse)
async def read_learningpath():
    with open("../Frontend/learning_path.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/preview", response_class=HTMLResponse)
async def preview():
    with open("../Frontend/preview.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/exercises", response_class=HTMLResponse)
async def read_exercises():
    with open("../Frontend/exercises.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/about_us", response_class=HTMLResponse)
async def read_about_us():
    with open("../Frontend/about_us.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/final_quiz", response_class=HTMLResponse)
async def read_final_quiz():
    with open("../Frontend/final_quiz.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/faqs", response_class=HTMLResponse)
async def read_faqs():
    with open("../Frontend/faqs.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


@app.get("/contact", response_class=HTMLResponse)
async def read_contact():
    with open("../Frontend/contact.html", "r", encoding="utf-8") as file:
        return HTMLResponse(content=file.read(), status_code=200)


@app.post("/chek-relevence")
def check_relevence(query: str):
    result = check_relevence_agent(model, query)
    return {"message": result}

@app.post("/skills-assessment")
def get_skills_assessment(query: str):
    try:
        result = check_relevence_agent(model, query)
        if result == "Relevant":
            skills_assessment_agent = SkillAssessmentAgent(model)
            result = skills_assessment_agent.generate_skill_assessment(query)
            return result
        else:
            return {"message": "Not relevant"}
    except Exception as e:
        return str(e)

@app.post("/skills-evaluation")
def skills_evaluation(skills_assessement: Skill, user_answers: List[str]):
    skills_evaluation_agent = SkillAssessmentEvaluator()
    evaluation = skills_evaluation_agent.evaluate(skills_assessement, user_answers)
    report = skills_evaluation_agent.generate_report(evaluation)
    return report

# Store the generated course plan in memory
course_plan_data = None

@app.post("/generate-course-plan")
def generate_course_plan(report: LearningPathInput):
    global course_plan_data
    learning_path_agent = LearningPathAgent(model=model)
    learning_path_result = learning_path_agent.generate_learning_path(report)
    course_plan_data = learning_path_result  # Store the generated course plan
    return learning_path_result

@app.get("/get-course-data")
async def get_course_data():
    global course_plan_data
    if course_plan_data is None:
        raise HTTPException(status_code=404, detail="Course plan data not found")
    return course_plan_data

@app.post("/generate-topic-content")
def generate_topic_content(topic_input: TopicInput):
    topic_content_agent = TopicContentAgent(model=model)
    topic_content_result = topic_content_agent.generate_topic_content(topic_input)
    return topic_content_result

class TopicRequest(BaseModel):
    topic_name: str

@app.post("/get-topic-resources")
def get_topic_resources(request: TopicRequest):
    print(f"Received topic_name: {request.topic_name}")  # Log the received topic_name
    resource_recommendation_agent = ResourceRecommendationAgent()
    resources = resource_recommendation_agent(request.topic_name)
    return resources

# Endpoint to handle questions
@app.post("/ask")
async def ask_question(question: QuestionRequest):
    """Endpoint to ask a question and return a simple text response."""
    # Initialize the agent
    agent = ChatTopicAgent(model, question.topics)
    try:
        result = agent.ask_question(question.question)
        if "error" in result:
            raise ValueError(result["error"])
        return SimpleResponse(response=result["answer"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/generate-exercises")
def generate_exercises(topics: List[Topic]):
    exercice_agent = ExerciseGenerator(model, topics)
    exercises = exercice_agent.generate_exercises()
    return exercises

@app.post("/generate_quiz")
async def generate_quiz(quiz_inputs: List[QuizInput]):
    try:
        quiz_content_agent = QuizContentAgent(model=model)
        quiz_items = []

        for quiz_input in quiz_inputs:
            quiz_content = quiz_content_agent.generate_quiz_content(quiz_input, 1)  # Generate 3 questions per module
            if quiz_content and quiz_content.questions:
                quiz_items.append(quiz_content)

        if not quiz_items:
            raise HTTPException(status_code=400, detail="No valid quiz content could be generated")

        return quiz_items

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@app.post("/correct-quiz")
def correct_quiz(user_answers: List[dict]):
    try:
        total_questions = sum(len(module.get('questions', [])) for module in user_answers)
        if total_questions == 0:
            raise HTTPException(status_code=400, detail="No questions provided")

        module_scores = {}
        total_score = 0

        for module_data in user_answers:
            module_name = module_data.get('module_name', 'Unknown Module')
            questions = module_data.get('questions', [])
            
            if questions:
                correct_count = sum(
                    1 for q in questions 
                    if set(q.get('user_answers', [])) == set(q.get('correct_answers', []))
                )
                module_score = (correct_count / len(questions)) * 100
                module_scores[module_name] = round(module_score, 1)
                total_score += module_score

        overall_score = round(total_score / len(user_answers), 1)

        return {
            "overall_score": overall_score,
            "module_scores": module_scores
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
