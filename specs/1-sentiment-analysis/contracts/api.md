# API Contract: Sentiment Analysis

This document defines the API for the backend sentiment analysis service.

## Endpoint: `/api/analyze`

- **Method**: `POST`
- **Description**: Triggers the sentiment analysis for a given YouTube video URL.

### Request Body

- **Content-Type**: `application/json`

**Schema**:

```json
{
  "url": "string",
  "comment_limit": "integer"
}
```

**Example**:

```json
{
  "url": "https://www.youtube.com/watch?v=Y2M4_Yx3a6U",
  "comment_limit": 1000
}
```

### Success Response (200 OK)

- **Content-Type**: `application/json`
- **Description**: Returns the full analysis report.
- **Schema**: The response will be a `VideoAnalysis` object as defined in `data-model.md`.

### Error Responses

- **400 Bad Request**: If the URL is invalid or missing.
- **404 Not Found**: If the video does not exist.
- **500 Internal Server Error**: For any other processing errors, including API failures.
