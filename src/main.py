from fastapi import FastAPI
from .routes import base, job_routes

app = FastAPI()


# app routes
app.include_router(base.base_router)
app.include_router(job_routes.enhance_position_router)