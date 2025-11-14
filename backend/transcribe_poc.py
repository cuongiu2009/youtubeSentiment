import whisper
import torch
from pytubefix import YouTube
import os

# Check if CUDA is available and set the device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# 1. Define YouTube URL
YOUTUBE_URL = "https://www.youtube.com/watch?v=EICd7f7kenk" # A 1-minute test video

try:
    # 2. Download Audio using Pytube
    print(f"Downloading audio for: {YOUTUBE_URL}")
    yt = YouTube(YOUTUBE_URL)
    
    # Get the best audio-only stream
    audio_stream = yt.streams.filter(only_audio=True).first()
    if not audio_stream:
        raise Exception("No audio stream found for this video.")

    # Download the audio stream to a temporary file
    output_file = audio_stream.download(output_path=".")
    base, ext = os.path.splitext(output_file)
    # Rename to a consistent name
    audio_file = base + '.mp3'
    os.rename(output_file, audio_file)
    print(f"Audio downloaded and saved to: {audio_file}")

    # 3. Transcribe with Whisper
    print("Loading Whisper model...")
    # Using the "base" model for a good balance of speed and accuracy
    model = whisper.load_model("base", device=DEVICE)

    print("Transcribing audio...")
    result = model.transcribe(audio_file, fp16=torch.cuda.is_available())
    
    # 4. Print the result
    print("\n--- TRANSCRIPT ---")
    print(result["text"])
    print("--------------------\n")

finally:
    # 5. Clean up the downloaded audio file
    if 'audio_file' in locals() and os.path.exists(audio_file):
        print(f"Cleaning up temporary file: {audio_file}")
        os.remove(audio_file)