from pydantic import BaseModel
from typing import List, Dict

class Comment(BaseModel):
    text: str
    stance: str

class VideoAnalysis(BaseModel):
    video_id: str
    title: str
    video_summary: str
    stance_distribution: Dict[str, float]
    comment_word_cloud: Dict[str, float] # Using a dict for word cloud data
    top_comments: List[Comment]
    full_comment_analysis: List[Comment]
