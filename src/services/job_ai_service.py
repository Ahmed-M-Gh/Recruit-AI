from .llm_client import get_llm_client
from src.config import get_settings, ResponseSignal
settings = get_settings()
from src.prompts import JOB_ENHANCEMENT_SYSTEM_PROMPT, JOB_ENHANCEMENT_USER_PROMPT
from src.schemas import EnhancePositionRequest, EnhancePositionResponse
import logging 
logger = logging.getLogger(__name__)
from fastapi import HTTPException, status
from openai import APIError, RateLimitError, APITimeoutError

class JobAIService:
    def __init__(self):
        self.client = get_llm_client()
        
    async def enhance_job_description(self, request: EnhancePositionRequest) -> EnhancePositionResponse:
        
        # Setting prompt for user
        user_prompt = JOB_ENHANCEMENT_USER_PROMPT.format(
            position_title=request.position_title,
            raw_description=request.raw_description
        )
        
        try:
                
            # Calling API and Obligate the response to be same as EnhancePositionResponse Schema.
            response = await self.client.beta.chat.completions.parse(
                model=settings.LLM_MODEL,
                messages=[
                    {"role" : "system", "content" : JOB_ENHANCEMENT_SYSTEM_PROMPT},
                    {"role" : "user", "content" : user_prompt},
                ],
                response_format=EnhancePositionResponse,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            # Return object ready
            return response.choices[0].message.parsed
        
        except RateLimitError:
            logger.error(ResponseSignal.RATE_LIMIT)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Our AI service is currently experiencing high traffic. Please try again in a few seconds."
            )
            
        except APITimeoutError:
            logging.error(ResponseSignal.API_TIME_OUT)
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="The AI provider took too long to respond. Please try again."
            )
            
        except Exception as e:
            logger.error(f"AI Enhancement Error : {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An Unexpected error occurred while processing the job description."
            )
            
            