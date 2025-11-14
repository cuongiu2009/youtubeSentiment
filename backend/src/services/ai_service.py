import whisper
import torch
from pytubefix import YouTube
import os
import tempfile
import subprocess
import json
import sys

from transformers import pipeline

# --- Constants ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Lazily load models to save resources. They will be loaded only when needed.
WHISPER_MODEL = None
SENTIMENT_PIPELINE = None

def _load_whisper_model():
    """Loads the Whisper model if it hasn't been loaded yet."""
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        print("Loading Whisper model for the first time...")
        WHISPER_MODEL = whisper.load_model("base", device=DEVICE)
        print(f"Whisper model loaded on device: {DEVICE}")

def _load_sentiment_pipeline():
    """Loads the sentiment analysis pipeline if it hasn't been loaded yet."""
    global SENTIMENT_PIPELINE
    if SENTIMENT_PIPELINE is None:
        print("Loading sentiment analysis pipeline for the first time...")
        SENTIMENT_PIPELINE = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if DEVICE == "cuda" else -1 # device=0 for cuda, -1 for cpu
        )
        print("Sentiment analysis pipeline loaded.")

def _transcribe_with_api(video_id: str) -> str:
    """
    (Method 1) Fetches a transcript by calling the youtube-transcript-api CLI
    as a subprocess.
    """
    print(f"Attempting to fetch transcript for video ID: {video_id} (Method 1 - Subprocess Workaround)")
    try:
        python_executable = sys.executable
        command = [
            python_executable,
            "-m",
            "youtube_transcript_api",
            "--languages",
            "vi",
            "en",
            "--format",
            "json",
            "--",
            video_id
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )

        if not result.stdout.strip():
            raise ValueError("Transcript API returned empty output.")

        # The data structure is a list containing one inner list of segments.
        transcript_data = json.loads(result.stdout)
        full_transcript = " ".join([segment['text'] for segment in transcript_data[0]])
        
        print("Successfully fetched transcript using Method 1 (Subprocess).")
        return full_transcript
    except subprocess.CalledProcessError as e:
        print(f"Subprocess for youtube-transcript-api failed. Stderr: {e.stderr}")
        raise e
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Could not get a valid transcript from Method 1. Error: {e}")
        raise e
    except Exception as e:
        print(f"An unexpected error occurred in the subprocess workaround: {e}")
        raise e

def _transcribe_with_whisper(url: str) -> str:
    """
    (Method 2) Downloads audio and transcribes it using Whisper.
    """
    _load_whisper_model() # Ensure the model is loaded
    print(f"Executing transcription with Whisper for: {url} (Method 2)")
    audio_file = None
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            raise Exception("No audio stream found for this video.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            audio_stream.stream_to_buffer(tmp_file)
            audio_file = tmp_file.name
        
        print(f"Audio downloaded to temporary file: {audio_file}")
        print("Transcribing audio with Whisper...")
        result = WHISPER_MODEL.transcribe(audio_file, fp16=torch.cuda.is_available())
        
        print("Transcription complete with Method 2.")
        return result["text"]
    finally:
        if audio_file and os.path.exists(audio_file):
            print(f"Cleaning up temporary file: {audio_file}")
            os.remove(audio_file)

def transcribe_youtube_video(url: str, method: str = "auto") -> str:
    """
    Transcribes a YouTube video based on the selected method.

    Args:
        url (str): The URL of the YouTube video.
        method (str): The transcription method. Can be one of:
                      - "auto" (default): Tries API first, falls back to Whisper.
                      - "api_only": Forces use of youtube-transcript-api.
                      - "whisper_only": Forces use of Whisper.

    Returns:
        The transcribed text of the video.
    """
    video_id = url.split("v=")[1].split("&")[0]

    if method == "api_only":
        return _transcribe_with_api(video_id)
    
    if method == "whisper_only":
        return _transcribe_with_whisper(url)

    # Default "auto" method
    try:
        return _transcribe_with_api(video_id)
    except Exception as e:
        print(f"Method 1 (API) failed: {e}. Falling back to Method 2 (Whisper).")
        return _transcribe_with_whisper(url)

def analyze_comment_sentiments(comments: list[str]) -> list[dict]:
    """
    Analyzes the sentiment of a list of comments, truncating long comments
    to fit the model's maximum input size.
    """
    _load_sentiment_pipeline() # Ensure the pipeline is loaded
    
    tokenizer = SENTIMENT_PIPELINE.tokenizer
    max_length = tokenizer.model_max_length

    # Truncate comments that are too long
    truncated_comments = []
    for comment in comments:
        tokens = tokenizer.encode(comment, truncation=True, max_length=max_length)
        truncated_comment = tokenizer.decode(tokens, skip_special_tokens=True)
        truncated_comments.append(truncated_comment)

    print(f"Analyzing sentiment for {len(truncated_comments)} comments (long ones truncated)...")
    
    # Process comments with a batch size of 1 to potentially avoid the 'int too big' error
    results = SENTIMENT_PIPELINE(truncated_comments, batch_size=1)
    
    # Combine the original comment with its result
    analyzed_comments = []
    for i, original_comment in enumerate(comments):
        analyzed_comments.append({
            "comment": original_comment,
            "sentiment": results[i]
        })
            
    print("Sentiment analysis complete.")
    return analyzed_comments
