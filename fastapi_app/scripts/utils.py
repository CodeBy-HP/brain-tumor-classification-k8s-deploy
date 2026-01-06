from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import os
import torch
from .logging import get_logger

logger = get_logger(__name__)


class ViTBrainTumorClassifier:
    CLASS_LABELS = {0: "Glioma", 1: "Meningioma", 2: "No Tumor", 3: "Pituitary"}
    
    def __init__(self, device: str = "cpu", model_name: str = "codeby-hp/vit-brain-tumor-classifier"):
        self.device = device
        self.model_name = model_name
        self.model = None
        self.processor = None
        self._load_model()
    
    def _load_model(self):
        try:
            logger.info(f"Downloading model from HuggingFace Hub: {self.model_name}")
            
            # Download from HuggingFace Hub
            self.processor = ViTImageProcessor.from_pretrained(self.model_name)
            self.model = ViTForImageClassification.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Model loading failed: {e}")
            raise
    
    def predict(self, image_path: str) -> dict:
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).item()
            confidence = probabilities[0, predicted_class].item()
            
            result = {
                "predicted_class": self.CLASS_LABELS.get(predicted_class, "Unknown"),
                "confidence": round(confidence * 100, 2),
                "all_predictions": {
                    self.CLASS_LABELS[i]: round(probabilities[0, i].item() * 100, 2)
                    for i in range(len(self.CLASS_LABELS))
                }
            }
            
            logger.info(f"Prediction: {result['predicted_class']} ({result['confidence']}%)")
            return result
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise