from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
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
    with open("../Frontend/index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)
    
@app.get("/evaluation", response_class=HTMLResponse)
async def read_index():
    with open("../Frontend/evaluation.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)
    
@app.get("/learningpath", response_class=HTMLResponse)
async def read_index():
    with open("../Frontend/learning_path.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)


@app.post("/chek-relevence")
def check_relevence(query: str):
    result = check_relevence_agent(model,query)
    return {"message": result}

@app.post("/skills-assessment")
def get_skills_assessment(query: str):
    try:
        result = check_relevence_agent(model,query)
        if result == "Relevant":
            skills_assessment_agent = SkillAssessmentAgent(model)
            result = skills_assessment_agent.generate_skill_assessment(query)
            return result
        else:
            return {"message": "Not relevant"}
    except Exception as e:
        return str(e)

@app.post("/skills-evaluation")
def skills_evaluation(skills_assessement:Skill,user_answers:List[str]):
    skills_evaluation_agent = SkillAssessmentEvaluator()
    evaluation = skills_evaluation_agent.evaluate(skills_assessement,user_answers)
    # return {"message": skills_assessement, "answers": user_answers}
    report=skills_evaluation_agent.generate_report(evaluation)
    return report

@app.post("/generate-course-plan")
def generate_course_plan(report:LearningPathInput):
    learning_path=report
    learning_path_agent=LearningPathAgent(model=model)
    learning_path_result=learning_path_agent.generate_learning_path(learning_path)
    return learning_path_result

@app.post("/generate-topic-content")
def generate_topic_content(topic_input:TopicInput):
    topic_content_agent=TopicContentAgent(model=model)
    topic_content_result=topic_content_agent.generate_topic_content(topic_input)
    return topic_content_result

@app.post("/get-topic-resources")
def get_topic_resources(topic_name:str):
    resource_recommendation_agent=ResourceRecommendationAgent()
    resources=resource_recommendation_agent(topic_name)
    return resources

# Endpoint to handle questions
@app.post("/ask")
async def ask_question(question: QuestionRequest):
    """Endpoint to ask a question and return a simple text response."""
    # Initialize the agent
    agent = ChatTopicAgent(model,question.topics)
    try:
        result = agent.ask_question(question.question)
        if "error" in result:
            raise ValueError(result["error"])
        return SimpleResponse(response=result["answer"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/generate-exercises")
def generate_exercises(topics:List[Topic]):
    exercice_agent=ExerciseGenerator(model,topics)
    exercises=exercice_agent.generate_exercises()
    return exercises




@app.post("/generate_quiz")
async def generate_quiz(quiz_inputs: List[QuizInput]):
    # Instantiate the agent with a model
    quiz_content_agent = QuizContentAgent(model=model)
    items = []
    for quiz_input in quiz_inputs:
        try:
            quiz_content = quiz_content_agent.generate_quiz_content(quiz_input, 5)
            items.append(quiz_content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return items

@app.post("/correct-quiz")
def correct_quiz(user_answers: List[QuizUserAnswers]):
    overall_score, module_scores = calculate_overall_score(user_answers)
    return {"overall_score": overall_score, "module_scores": module_scores}