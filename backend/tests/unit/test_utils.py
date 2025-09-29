from src.api.main import extract_video_id

def test_extract_video_id_standard():
    url = "https://www.youtube.com/watch?v=Y2M4_Yx3a6U"
    assert extract_video_id(url) == "Y2M4_Yx3a6U"

def test_extract_video_id_short():
    url = "https://youtu.be/Y2M4_Yx3a6U"
    assert extract_video_id(url) == "Y2M4_Yx3a6U"

def test_extract_video_id_embed():
    url = "https://www.youtube.com/embed/Y2M4_Yx3a6U"
    assert extract_video_id(url) == "Y2M4_Yx3a6U"

def test_extract_video_id_invalid():
    url = "https://www.notyoutube.com/watch?v=Y2M4_Yx3a6U"
    assert extract_video_id(url) is None
