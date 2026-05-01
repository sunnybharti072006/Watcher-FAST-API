import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from utils.text_cleaner import clean_text, truncate
from models.similarity import get_change_score
from models.summarizer import summarize
from models.action_advisor import get_action
import torch
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("AI Detective ML Service starting...")
    print(f"GPU Available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    yield
    print("Shutting down...")

app = FastAPI(
    title="AI Detective ML Service",
    description="Change detection + AI analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Request/Response Models
class AnalyzeRequest(BaseModel):
    url: str
    added_content: str = ""
    removed_content: str = ""

class AnalyzeResponse(BaseModel):
    has_significant_change: bool
    change_score: float
    summary: str
    recommended_action: str

# Endpoints
@app.get("/health")
def health():
    return {
        "status": "ok",
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU",
        "models": ["bart-large-cnn", "all-MiniLM-L6-v2", "flan-t5-base"]
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    try:
        # Clean text
        added   = clean_text(truncate(req.added_content))
        removed = clean_text(truncate(req.removed_content))

        # 1. Change Score
        score = get_change_score(
            req.removed_content,
            req.added_content
        )

        # 2. AI Summary
        summary = summarize(added, removed, req.url)

        # 3. Recommended Action
        action = get_action(summary, req.url)

        return AnalyzeResponse(
            has_significant_change=score > 0.1,
            change_score=score,
            summary=summary,
            recommended_action=action
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))