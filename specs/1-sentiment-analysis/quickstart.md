# Quickstart: Sentiment Analysis UI

This document describes how to use the sentiment analysis application.

## User Interface

The application will be a simple, single-page web interface with the following elements:

1.  **URL Input Field**: A text box where the user can paste the YouTube video URL.
2.  **Comment Limit Selector**: A dropdown menu allowing the user to select the number of comments to analyze (e.g., 500, 2000, 10000).
3.  **"Analyze" Button**: A button to submit the URL and start the analysis.
4.  **Results Display Area**: An area where the analysis report will be displayed once it's ready.

## Workflow

1.  **Paste URL**: The user pastes a valid YouTube video URL into the input field.
2.  **Select Limit**: The user chooses the desired comment limit.
3.  **Click Analyze**: The user clicks the "Analyze" button.
4.  **View Report**: The application will display a loading indicator while processing. Once complete, the results area will show:
    - The video title and AI-generated summary.
    - A pie chart of the sentiment distribution.
    - A word cloud of key topics from the comments.

## Testing Scenarios

- **Scenario 1 (Success)**: 
  - Paste a valid URL.
  - Select a limit.
  - Click "Analyze".
  - **Expected Result**: A full report is displayed.

- **Scenario 2 (Invalid URL)**:
  - Paste an invalid URL (e.g., "not-a-url").
  - Click "Analyze".
  - **Expected Result**: An error message is displayed.

- **Scenario 3 (Comments Disabled)**:
  - Paste a URL for a video with disabled comments.
  - Click "Analyze".
  - **Expected Result**: An error message stating that comments are disabled is displayed.
