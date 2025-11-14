import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# --- Constants ---
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    print("WARNING: YOUTUBE_API_KEY not found in .env file.")
    # You might want to raise an exception here in a real application
    # raise ValueError("YOUTUBE_API_KEY not found.")

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_video_details(video_id: str) -> dict:
    """
    Fetches details for a given YouTube video ID using the YouTube Data API v3.

    Args:
        video_id: The ID of the YouTube video.

    Returns:
        A dictionary containing video details (e.g., title, description).
        Returns None if the video is not found or an error occurs.
    """
    if not YOUTUBE_API_KEY:
        print("Cannot fetch video details without an API key.")
        return None

    try:
        youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_API_KEY
        )

        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if not response.get("items"):
            print(f"Video with ID '{video_id}' not found.")
            return None

        return response["items"][0]["snippet"]

    except Exception as e:
        print(f"An error occurred while fetching video details: {e}")
        return None

def get_video_comments(video_id: str, limit: int = 100) -> list[str]:
    """
    Fetches top-level comments for a given YouTube video ID.

    Args:
        video_id: The ID of the YouTube video.
        limit: The maximum number of comments to fetch.

    Returns:
        A list of comment texts.
    """
    if not YOUTUBE_API_KEY:
        print("Cannot fetch comments without an API key.")
        return []

    try:
        youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=YOUTUBE_API_KEY
        )

        comments = []
        next_page_token = None

        while len(comments) < limit:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, limit - len(comments)), # Fetch 100 or remaining
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break # No more pages

        print(f"Successfully fetched {len(comments)} comments.")
        return comments[:limit] # Ensure we don't exceed the limit

    except Exception as e:
        print(f"An error occurred while fetching comments: {e}")
        return []
