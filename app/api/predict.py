from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from app.models.model_handler import ModelHandler
from app.utils.logger import logger

router = APIRouter()

class InputData(BaseModel):
    rating: float = Field(..., example=4.5)
    day_of_week: str = Field(..., example="Monday")
    month: str = Field(..., example="January")
    region: str = Field(..., example="US")
    show_publisher: str = Field(..., example="Podcast Network")
    log10_duration: str = Field(..., example="3.5")
    log10_episodes: str = Field(..., example="2.0")
    explicit: bool = Field(..., example=False)
    is_externally_hosted: bool = Field(..., example=False)
    is_playable: bool = Field(..., example=True)
    language: str = Field(..., example="English")
    show_explicit: bool = Field(..., example=False)
    show_is_externally_hosted: bool = Field(..., example=False)
    show_media_type: str = Field(..., example="audio")

# Load the model using the ModelHandler
model_handler = ModelHandler()

@router.post("/predict")
async def predict(input_data: InputData):
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data.dict()])
        
        # Log incoming request data
        logger.info("Received prediction request with data: %s", input_data.dict())
        
        # Make prediction
        prediction = model_handler.predict(input_df)
        
        # Log prediction result
        logger.info("Prediction result: %s", prediction)
        
        return {"predicted_rank": int(prediction)}
    
    except Exception as e:
        logger.error("Prediction error: %s", str(e))
        raise HTTPException(status_code=500, detail="Prediction error occurred.")