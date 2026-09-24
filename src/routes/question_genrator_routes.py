from fastapi import APIRouter, Depends, HTTPException
from src.schemas import QuestionGeneratorRequest, InterviewQuestionsAPIResponse
from src.services import QuestionGeneratingService
import logging 
logger = logging.getLogger(__name__)

questions_generator_router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Interview Question"]
)

def get_question_generating_service() -> QuestionGeneratingService:
    return QuestionGeneratingService()


@questions_generator_router.post(
    "/generate-questions",
    response_model=InterviewQuestionsAPIResponse,
    response_model_exclude_none=True)
async def question_generator(
    request:QuestionGeneratorRequest,
    service: QuestionGeneratingService= Depends(get_question_generating_service)):
        try:
            logger.info(f"Generating '{request.question_type}' question for CV:{request.cv_id}")
            
            result = await service.generate_questions(request)
            return result
        
        except Exception as e:
            logger.error(f"ERROR generating question: {str(e)}")
            raise HTTPException(status_code=500, detail=f"CRITICAL ERROR: {str(e)}")