from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import sys
import os

# Add the parent directory to the sys.path to allow for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ai_service import transcribe_youtube_video, analyze_comment_sentiments
from services.youtube_service import get_video_details, get_video_comments

# Initialize the FastAPI app
app = FastAPI()

# --- Pydantic Models for Test Endpoints ---
class TranscriptionMethod(str, Enum):
    AUTO = "auto"
    API_ONLY = "api_only"
    WHISPER_ONLY = "whisper_only"

class TranscriptionRequest(BaseModel):
    url: str
    method: TranscriptionMethod = TranscriptionMethod.AUTO

class TranscriptionResponse(BaseModel):
    transcript: str

class SentimentRequest(BaseModel):
    comments: list[str]

# --- Test Endpoints ---

@app.post("/api/transcribe", response_model=TranscriptionResponse, tags=["Testing"])
async def transcribe_video_endpoint(request: TranscriptionRequest):
    """
    (Test Endpoint) Transcribes a YouTube video.
    """
    try:
        transcript_text = transcribe_youtube_video(request.url, method=request.method.value)
        return TranscriptionResponse(transcript=transcript_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-sentiments", tags=["Testing"])
async def analyze_sentiments_endpoint(request: SentimentRequest):
    """
    (Test Endpoint) Analyzes the sentiment of a list of comments.
    """
    try:
        results = analyze_comment_sentiments(request.comments)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/video-details", tags=["Testing"])
async def video_details_endpoint(url: str):
    """
    (Test Endpoint) Gets video details (title, description, etc.).
    """
    try:
        video_id = url.split("v=")[1].split("&")[0]
        details = get_video_details(video_id)
        if not details:
            raise HTTPException(status_code=404, detail="Video not found.")
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/comments", tags=["Testing"])
async def comments_endpoint(url: str, limit: int = 20):
    """
    (Test Endpoint) Gets video comments.
    """
    try:
        video_id = url.split("v=")[1].split("&")[0]
        comment_list = get_video_comments(video_id, limit)
        return {"comment_count": len(comment_list), "comments": comment_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", tags=["Default"])
def read_root():
    return {"message": "Welcome to the Sentiment Analysis API"}
