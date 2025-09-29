# Data Model: Sentiment Analysis

This document defines the data structures used in the sentiment analysis feature.

## VideoAnalysis

Represents the full analysis report for a single YouTube video.

**Attributes**:

- `video_id` (string): The unique ID of the YouTube video.
- `title` (string): The title of the YouTube video.
- `video_summary` (string): The AI-generated summary of the video's content (from Speech-to-Text).
- `sentiment_distribution` (object): An object showing the percentage of positive, negative, and neutral comments.
  - `positive` (float): Percentage of positive comments.
  - `negative` (float): Percentage of negative comments.
  - `neutral` (float): Percentage of neutral comments.
- `comment_word_cloud` (object): Data needed to generate a word cloud from comment text.
- `top_comments` (array[Comment]): A list of a few of the most representative or impactful comments.

## Comment

Represents a single YouTube comment included in the analysis.

**Attributes**:

- `text` (string): The text content of the comment.
- `sentiment` (string): The analyzed sentiment (`POSITIVE`, `NEGATIVE`, `NEUTRAL`).
