from fastapi import APIRouter, Depends
from src.schemas import CVScreeningRequest, CVScreeningResponse
from src.services import CVScreeningService

cv_screening_router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"]
)

# Using Depends to create instance
def get_screening_service():
    return CVScreeningService()

@cv_screening_router.post("/match-cv", response_model=CVScreeningResponse)
async def get_top_candidates(
    request:CVScreeningRequest,
    service:CVScreeningService = Depends(get_screening_service)
    ):
    
    filtered_cvs = service.get_top_k_candidates(
        job_description=request.job_description,
        cvs=request.cvs,
        top_k=request.top_k
    )
    
    if not filtered_cvs:
        return CVScreeningResponse(results=[])
    
    evaluated_cvs = await service.analyze_best_candidates(
        job_description=request.job_description,
        top_candidates=filtered_cvs
    )
    
    return evaluated_cvs