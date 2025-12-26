import warnings
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
import torch

from scripts.logging import get_logger
from scripts.utils import ViTBrainTumorClassifier
from scripts.data_model import ClassificationResponse, Prediction

warnings.filterwarnings("ignore")
logger = get_logger(__name__)

app = FastAPI(
    title="Brain Tumor Classification Inference API",
    description="Vision Transformer based brain tumor classification",
    version="1.0.0"
)

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
MODEL = None


@app.on_event("startup")
async def startup_event():
    global MODEL
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        MODEL = ViTBrainTumorClassifier(device=device)
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Failed to initialize model: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None,
        "version": "1.0.0"
    }


@app.post("/api/v1/classify")
async def classify_image(file: UploadFile = File(...)) -> ClassificationResponse:
    """
    Classify a brain tumor from an uploaded image.
    """
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        contents = await file.read()
        
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
        
        try:
            Image.open(tmp_path).verify()
        except Exception:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        try:
            logger.info(f"Processing: {file.filename}")
            prediction_result = MODEL.predict(tmp_path)
            
            response = ClassificationResponse(
                success=True,
                prediction=Prediction(
                    predicted_class=prediction_result["predicted_class"],
                    confidence=prediction_result["confidence"],
                    all_predictions=prediction_result["all_predictions"]
                ),
                message=f"Successfully classified as {prediction_result['predicted_class']}"
            )
            
            logger.info(f"Complete: {prediction_result['predicted_class']}")
            return response
            
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app:app", port=8000, reload=True, host="0.0.0.0")