from pydantic import BaseModel,Field
from typing import List

class ModuleContent(BaseModel):
  module_name:str=Field(description="Module Name")
  topics:List[str]=Field(description="List of Topics")
  milestone:str=Field(description="Milestone Description")


class LearningPath(BaseModel):
  student_level:str=Field(description="Student Level")
  course_name:str=Field(description="Course Name")
  learning_path:List[ModuleContent]

class LearningPathInput(BaseModel):
  course_name:str
  level:str
  score:float
  weaknesses:List[str]
  strengths:List[str]