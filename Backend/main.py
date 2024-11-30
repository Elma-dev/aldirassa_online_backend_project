from fastapi import FastAPI
from agents.agent_chek_relevence import *
from utils.check_model_status import *
from agents.skills_assessment_agent import *
from agents.skills_assessement_evaluator_agent import *
from entities.skills_entities import *
from entities.learning_path_entities import *
from agents.learning_path_agent import *
app = FastAPI()
model = get_model("gpt-4o-mini")
@app.get("/")
def read_root():
    return {"message": model_name}


@app.post("/chek-relevnce")
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
    report=skills_evaluation_agent.generate_report(evaluation)
    return report

@app.post("/generate-course-plan")
def generate_course_plan(report:LearningPathInput):
    learning_path=report
    learning_path_agent=LearningPathAgent(model=model)
    learning_path_result=learning_path_agent.generate_learning_path(learning_path)
    return learning_path_result