from fastedit.core.Media import _Media
import pytest

test_files = [
    1,
    "This_File_Does_Not_Exists.mp4",
    "./media/test_video_with_audio.mp4",
    "./media/test_audio.mp3",
    "./media/test_image.jpeg"
]

def test_media_path_with_number():
    with pytest.raises(TypeError) as error :
        _Media(test_files[0])
    assert str(error.value) == "Expected 'path' to be of type 'str', but got 'int' instead."

def test_media_path_with_does_not_exists():
    with pytest.raises(ValueError) as error :
        _Media(test_files[1])
    assert str(error.value) == "The specified path 'This_File_Does_Not_Exists.mp4' is invalid or does not exist."

def test_media_path_with_image():
    with pytest.raises(TypeError) as error :
        _Media(test_files[4])
    assert str(error.value) == "Invalid file type: Expected a video or audio file, got image file instead."

def test_media_path_with_video():
    media = _Media(test_files[2])
    assert isinstance(media, _Media)

def test_media_path_with_audio():
    media = _Media(test_files[3])
    assert isinstance(media, _Media)