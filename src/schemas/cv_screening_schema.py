from pydantic import BaseModel, Field
from typing import List

# ==============================
# Input Schema
# ==============================

class CVInput(BaseModel):
    cv_id:str = Field(..., description="Unique Identifier for the CV")
    cv_text:str = Field(..., description="The extracted text from the cv")
    
class CVScreeningRequest(BaseModel):
    job_description:str = Field(..., description="the text of the job Description")
    top_k:int = Field(5, description="Number of top CVs to return after semantic search")
    cvs: List[CVInput] = Field(..., description="List Of CVs to process")
    
# ==============================
# LLM Output Schema
# ==============================
class CVAIAnalysis(BaseModel):
    match_score:int = Field(..., description="Match percentage from 0 to 100")
    recommendation:str = Field(..., description="Must be one of : Strong Hire, Interview, Reject")
    matching_skills:List[str] = Field(..., description="Skills found in BOTH CV and Job Description")
    missing_skills:List[str] = Field(..., description="Important skills Required but missing from the CV")
    summary:str= Field(..., description="A Brief 2-sentence summary explaining the score")

# ==============================
# Output Schema
# ==============================
class CVResult(CVAIAnalysis):
    cv_id:str = Field(..., description="The ID of the evaluated CV")
    
class CVScreeningResponse(BaseModel):
    results: List[CVResult] = Field(..., description="The final list of evaluated CVs")