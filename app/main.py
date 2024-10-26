from fastapi import FastAPI
from app.core.config import settings
from app.api.predict import router as predict_router
from app.utils.logger import logger

app = FastAPI(
    title="POdcast rank Prediction API",
    description="API for predicting randk of the podcast base dont he current features.",
    version=settings.API_VERSION,
)

# Include the prediction router
app.include_router(predict_router, prefix="/api/v1")

@app.get("/")
async def health_check():
    logger.info("Health check endpoint accessed.")
    return {"health_check": "OK", "model_version": settings.MODEL_VERSION}
