from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import json
import os

from ..models.schemas import VideoAnalysis, Comment
from ..services.youtube_service import YouTubeService
from ..services.ai_service import AIService

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS Middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the API key from environment variables
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env file")

youtube_service = YouTubeService(api_key=API_KEY)
ai_service = AIService()

class AnalyzeRequest(BaseModel):
    url: str
    comment_limit: int = 100

def extract_video_id(url: str) -> str | None:
    """Extracts the YouTube video ID from a URL."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"(?:embed\/|v\/|youtu.be\/)([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.post("/api/analyze", response_model=VideoAnalysis)
async def analyze_video(request: AnalyzeRequest):
    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    try:
        # 1. Get Video Details & Content
        video_details = youtube_service.get_video_details(video_id)
        transcript = youtube_service.get_transcript(video_id)
        if not transcript:
            # Fallback to ASR model
            audio_path = youtube_service.download_audio(video_id)
            transcript = ai_service.transcribe_audio_file(audio_path)

        # Save the fetched transcript for review
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'reports'))
        os.makedirs(reports_dir, exist_ok=True)
        if transcript:
            transcript_file_path = os.path.join(reports_dir, f'{video_id}_transcript.txt')
            with open(transcript_file_path, 'w', encoding='utf-8') as f:
                f.write(transcript)

        if not transcript:
            transcript = "No transcript available for this video."
        video_summary = ai_service.summarize_text(transcript)
        
        # 2. Get Comments
        comments_text = youtube_service.get_video_comments(video_id, request.comment_limit)
        if not comments_text:
            raise HTTPException(status_code=400, detail="Could not retrieve comments or video has no comments.")

        # 3. Analyze Stance of comments relative to the video content
        stances = ai_service.analyze_stance(comments_text, video_summary)
        
        # 4. Process Results
        stance_counts = {"AGREEMENT": 0, "DISAGREEMENT": 0, "NEUTRAL": 0}
        top_comments = []
        full_analysis = []
        for i, result in enumerate(stances):
            stance = result['stance']
            stance_counts[stance] += 1
            
            analyzed_comment = Comment(text=comments_text[i], stance=stance)
            full_analysis.append(analyzed_comment)
            
            if len(top_comments) < 5:
                top_comments.append(analyzed_comment)

        total_stances = len(stances)
        stance_distribution = {k: (v / total_stances) * 100 for k, v in stance_counts.items()}

        # 5. Generate Word Cloud
        word_cloud_data = ai_service.generate_word_cloud_data(comments_text)

        # 6. Create the analysis object
        analysis_result = VideoAnalysis(
            video_id=video_id,
            title=video_details["title"],
            video_summary=video_summary,
            stance_distribution=stance_distribution,
            comment_word_cloud=word_cloud_data,
            top_comments=top_comments,
            full_comment_analysis=full_analysis
        )

        # 7. Save the result to a file
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'reports'))
        os.makedirs(reports_dir, exist_ok=True)
        file_path = os.path.join(reports_dir, f'{video_id}_analysis.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_result.model_dump(), f, ensure_ascii=False, indent=4)

        return analysis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))