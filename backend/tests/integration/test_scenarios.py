

def test_integration_success_scenario(client, mocker):
    """
    Tests the full success scenario using mocks.
    """
    # Mock the services
    mocker.patch(
        'src.api.main.youtube_service.get_video_details', 
        return_value={'title': 'Test Video', 'description': 'A test video.'}
    )
    mocker.patch(
        'src.api.main.youtube_service.get_video_comments',
        return_value=['This is a great comment!', 'This is a bad comment.']
    )
    mocker.patch(
        'src.api.main.ai_service.analyze_sentiment',
        return_value=[{'label': 'POSITIVE'}, {'label': 'NEGATIVE'}]
    )
    mocker.patch('src.api.main.transcribe_video_audio', return_value='A summary of the video.')
    mocker.patch('src.api.main.ai_service.summarize_text', return_value='A summary of the video.')
    mocker.patch('src.api.main.ai_service.generate_word_cloud_data', return_value={'great': 1, 'bad': 1})

    response = client.post("/api/analyze", json={"url": "https://www.youtube.com/watch?v=Y2M4_Yx3a6U", "comment_limit": 100})
    
    assert response.status_code == 200
    data = response.json()
    assert data["video_id"] == "Y2M4_Yx3a6U"
    assert data["title"] == "Test Video"
    assert "sentiment_distribution" in data

def test_integration_invalid_url(client):
    """
    Tests the invalid URL scenario. This doesn't need mocks.
    """
    response = client.post("/api/analyze", json={"url": "not-a-valid-url", "comment_limit": 100})
    assert response.status_code == 400

def test_integration_comments_disabled(client, mocker):
    """
    Tests the comments disabled scenario using a mock.
    """
    mocker.patch(
        'src.api.main.youtube_service.get_video_details', 
        return_value={'title': 'Test Video', 'description': 'A test video.'}
    )
    mocker.patch(
        'src.api.main.youtube_service.get_video_comments',
        side_effect=Exception("Comments are disabled")
    )

    video_with_disabled_comments = "https://www.youtube.com/watch?v=xxxxxxxxxxx"
    response = client.post("/api/analyze", json={"url": video_with_disabled_comments, "comment_limit": 100})
    assert response.status_code == 500
    assert "Comments are disabled" in response.json()["detail"]