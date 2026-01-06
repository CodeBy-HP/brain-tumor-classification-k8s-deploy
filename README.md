<div align="center">

# 🧠 Brain Tumor Classification API

*Fine-tuned Vision Transformer with AWS EKS Kubernetes orchestration, containerized deployment, and production-ready infrastructure*

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-AWS%20EKS-326CE5.svg)](https://kubernetes.io/)
[![AWS EKS](https://img.shields.io/badge/AWS-EKS%20%7C%20ECR-FF9900.svg)](https://aws.amazon.com/eks/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Transformers-EE4C2C.svg)](https://pytorch.org/)

</div>

---

## 🎯 Overview

A production-ready REST API for brain tumor classification using a **fine-tuned Vision Transformer (ViT) model**. The application is containerized with Docker and deployed on **AWS EKS (Kubernetes)**, featuring **automated CI/CD pipeline** with GitHub Actions for building and pushing Docker images to **Amazon ECR**.

---

## 🌈 Application UI

<div align="center">
<img width="493" height="858" alt="Application Interface" src="[PLACEHOLDER: Add your application screenshot]" />
</div>

---

## 🌈 Video Demo

<p align="center">
  <a href="[PLACEHOLDER: Add your video link]" target="_blank">
    <img 
      src="[PLACEHOLDER: Add video thumbnail]"
      alt="Watch Demo"
      width="700"
    />
  </a>
</p>

<p align="center"><b>▶️ Click to watch Kubernetes deployment & API demo</b></p>

---

## 🌈 Architecture Diagrams

<div align="center">

<img width="817" height="1056" alt="Kubernetes Architecture" src="[PLACEHOLDER: Add Kubernetes architecture diagram]" />
<img width="880" height="515" alt="Deployment Pipeline" src="[PLACEHOLDER: Add deployment pipeline diagram]" />

</div>

---

## ✨ Key Features

### 🧠 **VISION TRANSFORMER MODEL**
- State-of-the-art ViT architecture (google/vit-base-patch16-224-in21k)
- Fine-tuned on medical imaging dataset (brain tumor classification)
- Self-attention mechanism for precise tumor detection
- Transfer learning from ImageNet-21k pre-trained weights

### 🐳 **Docker & Container Support**
- Lightweight Python 3.10-slim base image
- Pre-cached model weights in Docker image for instant startup
- Non-root user for security
- Built-in HEALTHCHECK for container monitoring
- Multi-stage optimization for reduced image size

### ☸️ **Kubernetes Ready**
- Complete deployment manifest with resource requests/limits
- LoadBalancer service for external access
- Memory allocation: 1Gi requests / 2Gi limits
- CPU allocation: 500m requests / 1000m limits

### 🔄 **CI/CD Pipeline**
- GitHub Actions workflow for automated builds
- Automatic Docker image build on push to main/develop branches
- Push to Amazon ECR with SHA-based and latest tags
- AWS credential configuration via GitHub Secrets

---

## 🛠️ Tech Stack

- **Machine Learning:** PyTorch, Transformers, Vision Transformer (ViT)
- **Backend:** FastAPI
- **Container & Orchestration:** Docker, Kubernetes, AWS EKS
- **Container Registry:** Amazon ECR
- **Infrastructure:** AWS VPC, EC2
- **DevOps & CI/CD:** GitHub Actions, kubectl

---

## 📁 Project Structure

```
brain-tumor-classification/
├── fastapi_app/
│   ├── app.py                           # FastAPI application
│   ├── requirements.txt                 # Python dependencies
│   ├── models/
│   │   └── vit-brain-tumor-classifier/
│   │       ├── config.json              # ViT model config
│   │       ├── model.safetensors        # Fine-tuned weights
│   │       └── preprocessor_config.json # Image preprocessor config
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── data_model.py                # Pydantic response models
│   │   ├── logging.py                   # Logging configuration
│   │   └── utils.py                     # ViTBrainTumorClassifier class
│   ├── templates/
│   │   └── index.html                   # Web UI (Tailwind CSS)
│   └── logs/                            # Application logs
├── .github/workflows/
│   ├── build-and-push.yml               # GitHub Actions CI/CD pipeline
│   └── deployment.yaml                  # Kubernetes deployment manifest
├── Dockerfile                           # Docker image definition
└── README.md
```

---

## 🚀 API Endpoints

### Health Check
```http
GET /health
```
Returns model status and application version.

### Web Interface
```http
GET /
```
Serves the interactive image classification UI.

### Classification
```http
POST /api/v1/classify
Content-Type: multipart/form-data

file: <binary image data>
```

**Request**: Multipart form with image file (jpg, jpeg, png, gif, bmp)

**Response**:
```json
{
  "success": true,
  "prediction": {
    "predicted_class": "Glioma",
    "confidence": 94.32,
    "all_predictions": {
      "Glioma": 94.32,
      "Meningioma": 3.21,
      "No Tumor": 1.45,
      "Pituitary": 1.02
    }
  },
  "message": ""
}
```

---

## 📊 Model Details

- **Architecture**: Vision Transformer (ViT)
- **Base Model**: google/vit-base-patch16-224-in21k
- **Output Classes**: 4 tumor types (Glioma, Meningioma, No Tumor, Pituitary)
- **Input Size**: 224x224 RGB images
- **Model Source**: HuggingFace hub (codeby-hp/vit-brain-tumor-classifier)

---

## 📚 Learning Outcomes

- Vision Transformer (ViT) architecture and transfer learning
- FastAPI application development and REST API design
- Docker containerization with multi-stage builds
- Kubernetes deployment manifests and health probes
- AWS ECR for container image management
- GitHub Actions for CI/CD automation
- Container security best practices (non-root user, health checks)
- Production-ready API design patterns

---

## 🔮 Future Enhancements

- **GPU Acceleration:** Enable GPU support for faster and more efficient inference  
- **Batch Prediction:** High-throughput batch inference endpoints  
- **Auto Scaling:** Horizontal Pod Autoscaler (HPA) for dynamic workload scaling
- **A/B Testing:** Canary deployments for safe model comparison  
- **Advanced Monitoring:** Prometheus metrics and Grafana dashboards  

---

## 🌟 Why Kubernetes?

### Traditional Deployment vs. Kubernetes

| Aspect | Traditional VM | Kubernetes (EKS) |
|--------|----------------|------------------|
| **Container Orchestration** | Manual management | Automated scheduling & management |
| **Scaling** | Manual or basic auto-scaling | Supports HPA for auto-scaling (not yet configured) |
| **High Availability** | Configure load balancers manually | Built-in service discovery |
| **Deployment** | Manual rolling updates | Declarative, version-controlled rollouts |
| **Self-Healing** | Manual restart required | Automatic pod recovery |
| **Resource Efficiency** | Fixed resource allocation | Dynamic resource optimization |
| **Cost Optimization** | Always-on infrastructure | Fine-grained resource control |

---

## 👤 Author

**Harsh Patel**  
📧 code.by.hp@gmail.com  
🔗 [GitHub](https://github.com/CodeBy-HP) • [LinkedIn](https://www.linkedin.com/in/harsh-patel-389593292/)

---

<div align="center">

**⭐ If you find this project helpful, please star it!**

</div>