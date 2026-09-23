from fastapi import FastAPI
from .routes import base, job_routes, cv_screening

app = FastAPI()


# app routes
app.include_router(base.base_router)
app.include_router(job_routes.enhance_position_router)
app.include_router(cv_screening.cv_screening_router)