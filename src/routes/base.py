from fastapi import APIRouter, Depends
from src.config import Settings, get_settings

# APP Rout
base_router = APIRouter(
    prefix="/api/v1",
    tags=["base_endpoint"]
)

# Base Endpoint
@base_router.get("/")
async def get_information(app_info:Settings = Depends(get_settings)):    
    return {
        "app_name" : app_info.APP_NAME,
        "app_version" : app_info.APP_VERSION,
    }