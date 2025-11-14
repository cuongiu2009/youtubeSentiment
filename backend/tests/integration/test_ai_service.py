import pytest
import sys
import os

# Add the project's 'src' directory to the Python path
# to allow imports of our service modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from services.ai_service import transcribe_youtube_video

def test_transcribe_youtube_video_success():
    """
    Tests the successful transcription of a short YouTube video.
    This is an integration test as it calls external services (YouTube)
    and uses a loaded model.
    """
    # A short, reliable video for testing
    test_url = "https://www.youtube.com/watch?v=EICd7f7kenk"
    
    # Execute the function
    transcript = transcribe_youtube_video(test_url)
    
    # Assert the results
    assert isinstance(transcript, str)
    assert len(transcript) > 50 # Check that the transcript is not empty or trivial
    assert "Gmini V3" in transcript # Check for a specific keyword known to be in the video
