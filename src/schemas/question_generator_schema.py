from pydantic import BaseModel, Field
from typing import List, Literal, Optional


# Shared Schemas
class QuestionFormat(BaseModel):
    question: str = Field(..., description="A generated question")
    difficulty: Literal["Easy", "Medium", "Hard"] = Field(..., description="Must be exactly: Easy, Medium, or Hard")
    green_flags: List[str] = Field(..., description="A list of Green flags for answers")
    red_flags: List[str] = Field(..., description="A list of Red flags for answers")
    
# Request Schema
class QuestionGeneratorRequest(BaseModel):
    cv_id: str = Field(..., description="Unique Identifier for the CV")
    cv_text: str = Field(..., description="The extracted text from the CV")
    job_description: str = Field(..., description="The text of the Job Description")
    
    question_type: Literal["all", "technical", "behavioral", "gap"] = Field(
        ..., description="Must be one of: all, technical, behavioral, gap"
    )
    
    matching_skills: List[str] = Field(default=[], description="Skills found in BOTH CV and Job Description")
    missing_skills: List[str] = Field(default=[], description="Important skills required but missing from the CV")
    previous_questions: List[str] = Field(default=[], description="List of previously generated questions to avoid duplication")
    
# Internal LLM Schema
class QuestionGeneratorResponse(BaseModel):
    question_type: str = Field(..., description="Will be one of: technical, behavioral, gap")
    questions: List[QuestionFormat] = Field(..., description="A list of generated questions")
    
# Final API Response
class InterviewQuestionsAPIResponse(BaseModel):
    cv_id: str
    technical_questions: Optional[List[QuestionFormat]] = None
    behavioral_questions: Optional[List[QuestionFormat]] = None
    gap_questions: Optional[List[QuestionFormat]] = None