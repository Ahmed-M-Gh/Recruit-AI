from pydantic import BaseModel

class EnhancePositionRequest(BaseModel):
    position_title:str
    raw_description:str

class EnhancePositionResponse(BaseModel):
    enhanced_description:str
    extracted_skills:list[str]  