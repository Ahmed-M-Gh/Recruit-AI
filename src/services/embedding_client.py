from sentence_transformers import SentenceTransformer
from src.config import get_settings
import logging
logger = logging.getLogger(__name__)
settings = get_settings()
_embedding_model = None

def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    
    if _embedding_model is None:
        logger.info(f"Loading Embedding Model '{settings.EMBEDDING_MODEL}' into memory... this might take a few seconds.")
        
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Embedding Model loaded successfully!")
    return _embedding_model