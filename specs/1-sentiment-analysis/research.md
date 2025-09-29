# Research: Sentiment Analysis Feature

This document outlines the research required to make key technical decisions for the sentiment analysis feature.

## 1. Speech-to-Text Service

**Goal**: Select the most appropriate Speech-to-Text (STT) service for transcribing YouTube video audio.

**Options**:
1.  **YouTube Transcript API**: 
    - *Pros*: Potentially free, fastest option, no separate processing required.
    - *Cons*: May not be available for all videos, quality can vary.
2.  **Google Cloud Speech-to-Text**:
    - *Pros*: High accuracy, supports many languages, robust API.
    - *Cons*: Can be expensive at scale.
3.  **OpenAI Whisper**:
    - *Pros*: State-of-the-art accuracy, open-source (can be self-hosted).
    - *Cons*: Requires more setup and infrastructure management if self-hosted.

**Decision**: 
- **Primary**: Attempt to use the **YouTube Transcript API** first via a direct API call. This is the most efficient method.
- **Fallback**: If no transcript is available, use **OpenAI Whisper**. This requires downloading the audio stream first using the `pytube` library.

## 2. Sentiment Analysis Model

**Goal**: Select a pre-trained sentiment analysis model from the Hugging Face Hub.

**Options**:
1.  **`distilbert-base-uncased-finetuned-sst-2-english`**: A lightweight and fast model, good for general-purpose sentiment analysis.
2.  **`cardiffnlp/twitter-roberta-base-sentiment`**: A model specifically trained on social media text (Twitter), which is similar in nature to YouTube comments.
3.  **`nlptown/bert-base-multilingual-uncased-sentiment`**: A model that supports multiple languages, which could be useful for analyzing comments in various languages.

**Decision**: Start with **`cardiffnlp/twitter-roberta-base-sentiment`** as it is trained on data that is structurally similar to YouTube comments, which should yield better results.

## 3. YouTube API Best Practices

**Goal**: Understand the best practices for using the YouTube Data API v3 to avoid quota issues and handle errors.

**Key Areas to Investigate**:
- **Quota Costs**: Determine the quota cost for fetching video details and comments.
- **Pagination**: Implement proper pagination for fetching comments.
- **Error Handling**: Implement robust error handling for common API errors (e.g., `videoNotFound`, `commentsDisabled`).

**Decision**: The implementation will use the official `google-api-python-client` library and will include logic to handle pagination and API errors gracefully. Quota usage will be monitored during development.
