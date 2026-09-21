from fastapi import FastAPI
from .routes import base

app = FastAPI()


# app routes
app.include_router(base.base_router)