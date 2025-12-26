import re
from fastapi import FastAPI

app = FastAPI(title="Brain Tumor Classification Inference API")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)