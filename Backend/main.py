from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from agents.agent_chek_relevence import *
from utils.check_model_status import *
from agents.skills_assessment_agent import *
from agents.skills_assessement_evaluator_agent import *
from entities.skills_entities import *
from entities.learning_path_entities import *
from fastapi.responses import HTMLResponse

from agents.learning_path_agent import *
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