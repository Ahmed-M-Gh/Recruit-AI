from .llm_client import get_llm_client
from typing import List
from src.config import get_settings
settings = get_settings()
from src.schemas import CVInput, CVAIAnalysis, CVResult, CVScreeningResponse
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from src.prompts import CV_EVALUATOR_SYSTEM_PROMPT, CV_EVALUATOR_USER_PROMPT
import logging
logger = logging.getLogger(__name__)
import asyncio
from .embedding_client import get_embedding_model

class CVScreeningService:
    def __init__(self):
        self.embedding_model = get_embedding_model()
        self.llm_client = get_llm_client()
    
    def get_top_k_candidates(self, job_description:str, cvs:List[CVInput], top_k:int) -> list[CVInput]:
        """convert text to vector and calculate the similarity to get be candidates"""
        if not cvs:
            return []
        
        cv_texts = [cv.cv_text for cv in cvs]
        
        # Embedding the job and cv text
        job_embeddings = self.embedding_model.encode([job_description])
        cv_embeddings = self.embedding_model.encode(cv_texts)
        
        # similarities
        similarities = cosine_similarity(job_embeddings, cv_embeddings)[0]
        
        top_k_indices = np.argsort(similarities)[::-1][:top_k]
        
        top_candidates = [cvs[i] for i in top_k_indices]
        
        return top_candidates
    
    
    async def evaluate_sing_cv_(self, cv: CVInput, job_description:str) -> CVResult:
        """Evaluate cv of candidates"""
        user_prompt = CV_EVALUATOR_USER_PROMPT.format(
            job_description=job_description,
            cv_text=cv.cv_text
        )
        
        try : 
            # Calling API and Obligate the response to be same as EnhancePositionResponse Schema.
            response = await self.llm_client.beta.chat.completions.parse(
                model = settings.LLM_MODEL,
                messages=[
                    {"role" : "system", "content" : CV_EVALUATOR_SYSTEM_PROMPT},
                    {"role" : "user", "content" : user_prompt}
                ],
                response_format=CVAIAnalysis,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )
            
            # Extract result from llm
            ai_analysis = response.choices[0].message.parsed
            
            return CVResult(
                cv_id = cv.cv_id,
                match_score=ai_analysis.match_score,
                recommendation=ai_analysis.recommendation,
                matching_skills=ai_analysis.matching_skills,
                missing_skills=ai_analysis.missing_skills,
                summary=ai_analysis.summary
            )
            
        
        except Exception as e:
            
            # Fault Tolerance
            logger.error(f"Failed to evaluate CV {cv.cv_id} : {str(e)}")
            
            return CVResult(
                cv_id = cv.cv_id,
                match_score=0,
                recommendation="Reject",
                matching_skills=[],
                missing_skills=[],
                summary="System Error : Could not process this CV due to AI Service timeout or limits."
            )
    
    
    async def analyze_best_candidates(self, job_description:str, top_candidates:List[CVInput]) -> CVScreeningResponse:
        """Looping on all candidates async"""
        tasks = []
        
        # loop on all top candidates
        for candidate in top_candidates:
            tasks.append(self.evaluate_sing_cv_(cv=candidate, job_description=job_description))
        
        evaluated_cvs = await asyncio.gather(*tasks)
        
        return CVScreeningResponse(results=evaluated_cvs)