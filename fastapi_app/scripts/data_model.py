from pydantic import BaseModel, Field
from typing import Dict


class Prediction(BaseModel):
    predicted_class: str = Field(..., description="Predicted tumor class")
    confidence: float = Field(..., description="Confidence percentage (0-100)")
    all_predictions: Dict[str, float] = Field(..., description="Confidence scores for all classes")


class ClassificationResponse(BaseModel):
    success: bool = Field(..., description="Whether classification was successful")
    prediction: Prediction = Field(..., description="Classification results")
    message: str = Field(default="", description="Additional message or error info")





