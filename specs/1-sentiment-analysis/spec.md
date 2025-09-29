# Feature Specification: Sentiment Analysis for a Specific YouTube Video

**Feature Branch**: `feature/1-sentiment-analysis`  
**Created**: 2025-09-25  
**Status**: Clarified  
**Input**: User description: "Sentiment analysis for a specific YouTube video using its URL"

---

## Clarifications

### Session 2025-09-25
- Q: For the initial version, what level of video content analysis should be implemented? → A: Text-Based Analysis: Use a Speech-to-Text service to get a transcript of the video.
- Q: How should the system behave if a YouTube video has its comments disabled? → A: Show an Error Message: Display a clear message like "This video has comments disabled, so sentiment analysis is not possible." and stop processing.
- Q: To manage costs and processing time, how should we handle videos with a very large number of comments? → A: User-Selectable Limit: Allow the user to choose how many comments to analyze from predefined tiers.
- Q: What should happen if the YouTube API is unavailable or returns an error during the process? → A: Display a Generic Error: Show a simple, non-technical error message like, "Could not connect to YouTube. Please try again later."

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a user, I want to paste a YouTube video URL and receive a detailed sentiment analysis report, so that I can understand the community's reaction to the video's content.

### Acceptance Scenarios
1. **Given** a valid YouTube video URL, **When** the user submits it, **Then** the system should display a report with a video summary, sentiment analysis of the comments, and key topics.
2. **Given** an invalid URL, **When** the user submits it, **Then** the system should display an error message.

### Edge Cases
- If a video has comments disabled, the system MUST display a clear error message and stop processing.
- The system MUST allow the user to select from predefined tiers for the number of comments to analyze.
- If the YouTube API is unavailable, the system MUST display a generic, non-technical error message.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST accept a YouTube video URL as input.
- **FR-002**: The system MUST use the YouTube API to fetch video details and comments.
- **FR-003**: The system MUST perform sentiment analysis on the comments, categorizing them as positive, negative, or neutral.
- **FR-004**: The system MUST use a Speech-to-Text service to generate a summary of the video's spoken content.
- **FR-005**: The system MUST display a report including the video summary, a sentiment distribution chart (e.g., pie chart), and a word cloud of key topics from the comments.
- **FR-006**: The system MUST present the user with predefined tiers (e.g., 500, 2000, 10000) to limit the number of comments for analysis.

### Key Entities *(include if feature involves data)*
- **Video**: Represents a YouTube video with attributes like URL, title, and summary.
- **Comment**: Represents a user comment with attributes like text and sentiment.

---

## Review & Acceptance Checklist
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous  

---
