import requests
import re
import os
import yt_dlp
from typing import List, Dict, Optional

class YouTubeService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"

    def _parse_srt(self, srt_content: str) -> str:
        """A simple function to parse SRT content and extract plain text."""
        lines = srt_content.strip().split('\n')
        text_lines = [line for line in lines if not (line.isdigit() or '-->' in line or line == '')]
        return ' '.join(text_lines)

    def get_transcript(self, video_id: str) -> Optional[str]:
        """Fetches the transcript for a video if available."""
        # This API often requires OAuth and fails with simple API keys. 
        # We will rely on the yt-dlp fallback.
        return None

    def download_audio(self, video_id: str) -> Optional[str]:
        """Downloads and converts audio to mp3 using yt-dlp and a specified FFmpeg path."""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            temp_dir = os.path.join(backend_dir, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            output_template = os.path.join(temp_dir, f'{video_id}.mp3')
            # Correct, absolute path to the ffmpeg executable
            ffmpeg_executable = r"C:\ffmpeg\bin\ffmpeg.exe"
            # Correct, absolute path to the cookies file
            cookies_path = r"C:\Users\Lenovo\Desktop\Code\Python\youtubeSentiment\backend\src\api\cookies.txt"

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': ffmpeg_executable,
                'outtmpl': os.path.join(temp_dir, f'{video_id}'),
                'cookiefile': cookies_path,
                'quiet': True,
                'no_warnings': True,
            }

            if os.path.exists(output_template):
                os.remove(output_template)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if os.path.exists(output_template):
                return output_template
            else:
                print(f"ERROR: yt-dlp (library) ran but the output file was not found at {output_template}")
                return None

        except Exception as e:
            print(f"An unexpected error occurred during audio download with yt-dlp library: {e}")
            return None

    def get_video_details(self, video_id: str) -> Dict:
        """Fetches video details from YouTube API."""
        params = {'part': 'snippet', 'id': video_id, 'key': self.api_key}
        response = requests.get(f'{self.base_url}/videos', params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get("items"): raise Exception("Video not found")
        item = data["items"][0]["snippet"]
        return {"title": item["title"], "description": item["description"]}

    def get_video_comments(self, video_id: str, max_results: int) -> List[str]:
        """Fetches comments for a video."""
        comments = []
        next_page_token = None
        try:
            while len(comments) < max_results:
                params = {
                    'part': 'snippet',
                    'videoId': video_id,
                    'maxResults': min(max_results - len(comments), 100),
                    'textFormat': 'plainText',
                    'key': self.api_key,
                    'pageToken': next_page_token
                }
                response = requests.get(f'{self.base_url}/commentThreads', params=params)
                response.raise_for_status()
                data = response.json()

                for item in data['items']:
                    comments.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                
                next_page_token = data.get('nextPageToken')
                if not next_page_token: break
            return comments
        except requests.exceptions.HTTPError as e:
            if "commentsDisabled" in e.response.text: raise Exception("Comments are disabled for this video.")
            raise e
