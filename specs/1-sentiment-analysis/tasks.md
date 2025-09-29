# Tasks: Sentiment Analysis for a Specific YouTube Video

**Input**: Design documents from `/specs/1-sentiment-analysis/`

This task list is broken down into phases. Tasks marked with `[P]` can be worked on in parallel.

## Phase 1: Setup

- [ ] **T001**: Create the project directory structure (`backend/` and `frontend/`).
- [ ] **T002**: Initialize the backend Python project with a `pyproject.toml` file. Include `fastapi`, `uvicorn`, `google-api-python-client`, `transformers`, `torch`, and a library for `Whisper`.
- [ ] **T003**: Initialize the frontend project with `npm init -y` and install basic dependencies for a vanilla JS/HTML setup.
- [ ] **T004**: [P] Configure `ruff` for linting the backend Python code.
- [ ] **T005**: [P] Configure `eslint` and `prettier` for the frontend JavaScript code.
- [ ] **T005b**: Add `pytube` and `openai-whisper` to the backend dependencies in `pyproject.toml`.

## Phase 2: Backend Development (Tests First)

**CRITICAL: Test tasks must be completed before their corresponding implementation tasks.**

- [ ] **T006**: [P] Write a failing contract test for the `POST /api/analyze` endpoint in `backend/tests/contract/test_api.py`.
- [ ] **T007**: [P] Write failing integration tests in `backend/tests/integration/` for the scenarios in `quickstart.md` (success, invalid URL, comments disabled).
- [ ] **T008**: Implement the Pydantic models for `VideoAnalysis` and `Comment` in `backend/src/models/schemas.py` based on `data-model.md`.
- [ ] **T009**: Implement a service in `backend/src/services/youtube_service.py` to handle all interactions with the YouTube Data API (fetching video details and comments).
- [ ] **T010**: Implement a service in `backend/src/services/ai_service.py` that contains the logic for:
    - Transcribing audio with Whisper.
    - Analyzing sentiment with `cardiffnlp/twitter-roberta-base-sentiment`.
- [ ] **T010b**: Implement the fallback logic in `ai_service.py` to use `pytube` to download audio and `Whisper` to transcribe it when a YouTube transcript is not available.
- [ ] **T011**: Implement the `POST /api/analyze` endpoint in `backend/src/api/main.py`. This endpoint will orchestrate calls to the YouTube and AI services.
- [ ] **T012**: Ensure all backend tests written in T006 and T007 are now passing.

## Phase 3: Frontend Development

- [ ] **T013**: Create the main HTML file (`frontend/src/index.html`) with the basic UI elements described in `quickstart.md` (input, dropdown, button, results area).
- [ ] **T014**: Create a JavaScript file (`frontend/src/app.js`) to handle the frontend logic.
- [ ] **T015**: Implement the `fetch` call in `app.js` to send the YouTube URL to the backend `POST /api/analyze` endpoint when the button is clicked.
- [ ] **T016**: Implement the logic to display a loading indicator while the backend is processing the request.
- [ ] **T017**: Implement the logic to receive the JSON response from the backend and display the results dynamically in the results area.
- [ ] **T018**: [P] Add basic CSS styling in `frontend/src/style.css` to ensure the application is usable and looks clean.

## Phase 4: Polish & Documentation

- [ ] **T019**: [P] Add unit tests for any complex utility functions or business logic in the backend.
- [ ] **T020**: [P] Update the main `README.md` with instructions on how to set up and run the project.
- [ ] **T021**: Manually test the end-to-end flow using the scenarios from `quickstart.md` to ensure everything works as expected.
