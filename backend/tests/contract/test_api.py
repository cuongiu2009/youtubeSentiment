

def test_analyze_endpoint_exists(client):
    """ 
    Tests that a POST to /api/analyze doesn't return 404.
    """
    response = client.post("/api/analyze", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "comment_limit": 100})
    # The endpoint exists, so it won't be a 404, even if it errors out internally
    assert response.status_code != 404, "Endpoint /api/analyze not found!"

def test_analyze_endpoint_success(client, mocker):
    """
    Tests that the endpoint returns a 200 OK when services are mocked.
    """
    # Mock all external calls
    mocker.patch('src.api.main.youtube_service.get_video_details', return_value={'title': 'Test Video'})
    mocker.patch('src.api.main.youtube_service.get_video_comments', return_value=['comment1'])
    mocker.patch('src.api.main.ai_service.analyze_sentiment', return_value=[{'label': 'NEUTRAL'}])
    mocker.patch('src.api.main.transcribe_video_audio', return_value='summary')
    mocker.patch('src.api.main.ai_service.summarize_text', return_value='summary')
    mocker.patch('src.api.main.ai_service.generate_word_cloud_data', return_value={})

    response = client.post("/api/analyze", json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "comment_limit": 100})
    
    assert response.status_code == 200
    assert "video_id" in response.json()