from fastapi import APIRouter, Depends
from src.schemas import EnhancePositionRequest, EnhancePositionResponse
from src.services import JobAIService

# The route
enhance_position_router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"]
)

# Using Depends to create instance
def get_job_ai_service():
    return JobAIService()

@enhance_position_router.post("/enhance-position", response_model=EnhancePositionResponse)
async def enhance_position_description(
    request:EnhancePositionRequest,
    service:JobAIService = Depends(get_job_ai_service)):
    
    response = await service.enhance_job_description(request)
    return response
    