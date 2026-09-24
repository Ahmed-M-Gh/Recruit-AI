import asyncio
from typing import Dict, Any
from src.config import get_settings
from .llm_client import get_llm_client
from src.schemas import (
    QuestionGeneratorRequest,
    QuestionGeneratorResponse
)
from src.prompts import (
    TECHNICAL_QUESTION_GENERATING_SYSTEM_PROMPT,
    BEHAVIORAL_QUESTION_GENERATING_SYSTEM_PROMPT,
    GAP_QUESTION_GENERATING_SYSTEM_PROMPT,
    QUESTION_GENERATING_USER_PROMPT
)

class QuestionGeneratingService:
    def __init__(self):
        
        self.llm_client = get_llm_client()
        self.settings = get_settings()
        
        self.model_name = self.settings.LLM_MODEL
        
    def _build_user_prompt(self, request: QuestionGeneratorRequest) -> str:
        """Helper method to format the user prompt safely with fallbacks."""
        prev_qs = request.previous_questions
        prev_qs_text = "\n".join(prev_qs) if prev_qs else "None. This is the first generation."
        
        matching = ", ".join(request.matching_skills) if request.matching_skills else "None"
        missing = ", ".join(request.missing_skills) if request.missing_skills else "None"
        
        return QUESTION_GENERATING_USER_PROMPT.format(
            job_description=request.job_description,
            cv_text=request.cv_text,
            matching_skills=matching,
            missing_skills=missing,
            previous_questions=prev_qs_text
        )

    async def _call_llm(self, system_prompt: str, user_prompt: str) -> QuestionGeneratorResponse:
        """Helper method to call OpenAI and enforce the Pydantic schema."""
        schema_instruction = (
            "\n\nOUTPUT FORMAT:\n"
                "You MUST return a valid JSON object. Do not wrap it in markdown block quotes. "
                "The JSON must strictly match this structure:\n"
                '{\n'
                '  "question_type": "string",\n'
                '  "questions": [\n'
                '    {\n'
                '      "question": "string",\n'
                '      "difficulty": "Easy",\n'
                '      "green_flags": ["string"],\n'
                '      "red_flags": ["string"]\n'
                '    }\n'
                '  ]\n'
                '}'
            )
        completion = await self.llm_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role" : "system" , "content" : system_prompt + schema_instruction},
                {"role" : "user" , "content" : user_prompt}
            ],
            response_format={"type" : "json_object"},
            temperature=self.settings.LLM_TEMPERATURE
        )
        raw_js_str = completion.choices[0].message.content
        try:
            return QuestionGeneratorResponse.model_validate_json(raw_js_str)
        except Exception as e:
            print(f"Failed to parse LLM Output. Raw output: {raw_js_str}")
            raise ValueError(f"LLM returned invalid JSON schema : {str(e)}")
        

    async def get_technical_questions(self, request: QuestionGeneratorRequest) -> QuestionGeneratorResponse:
        user_prompt = self._build_user_prompt(request)
        response = await self._call_llm(TECHNICAL_QUESTION_GENERATING_SYSTEM_PROMPT, user_prompt)
        response.question_type = "technical"
        return response
    
    async def get_behavior_questions(self, request: QuestionGeneratorRequest) -> QuestionGeneratorResponse:
        user_prompt = self._build_user_prompt(request)
        response = await self._call_llm(BEHAVIORAL_QUESTION_GENERATING_SYSTEM_PROMPT, user_prompt)
        response.question_type = "behavioral"
        return response
    
    async def get_gap_questions(self, request: QuestionGeneratorRequest) -> QuestionGeneratorResponse:
        user_prompt = self._build_user_prompt(request)
        response = await self._call_llm(GAP_QUESTION_GENERATING_SYSTEM_PROMPT, user_prompt)
        response.question_type = "gap"
        return response
    
    

    async def generate_questions(self, request: QuestionGeneratorRequest) -> Dict[str, Any]:
        if request.question_type == "technical":
            res = await self.get_technical_questions(request)
            return {
                "cv_id": request.cv_id, 
                "technical_questions": [q.model_dump() for q in res.questions]
            }
        
        elif request.question_type == "behavioral":
            res = await self.get_behavior_questions(request)
            return {
                "cv_id": request.cv_id, 
                "behavioral_questions": [q.model_dump() for q in res.questions]
            }
        
        elif request.question_type == "gap":
            res = await self.get_gap_questions(request)
            return {
                "cv_id": request.cv_id, 
                "gap_questions": [q.model_dump() for q in res.questions]
            }
        
        elif request.question_type == "all":
            tech_res, behav_res, gap_res = await asyncio.gather(
                self.get_technical_questions(request),
                self.get_behavior_questions(request),
                self.get_gap_questions(request)
            )
            
            return {
                "cv_id": request.cv_id,
                "technical_questions": [q.model_dump() for q in tech_res.questions],
                "behavioral_questions": [q.model_dump() for q in behav_res.questions],
                "gap_questions": [q.model_dump() for q in gap_res.questions]
            }