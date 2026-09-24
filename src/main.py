from fastapi import FastAPI
from .routes import base, job_routes, cv_screening_routes, question_genrator_routes
app = FastAPI()


# app routes
app.include_router(base.base_router)
app.include_router(job_routes.enhance_position_router)
app.include_router(cv_screening_routes.cv_screening_router)
app.include_router(question_genrator_routes.questions_generator_router)