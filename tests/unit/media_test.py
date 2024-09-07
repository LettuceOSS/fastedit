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
    with pytest.raises(TypeError) as error:
        _Media(test_files[0])
    expected_error = (
        "Expected 'path' to be of type 'str', but got 'int' instead."
    )
    assert str(error.value) == expected_error


def test_media_path_with_does_not_exists():
    with pytest.raises(ValueError) as error:
        _Media(test_files[1])
    expected_error = (
        "The specified path 'This_File_Does_Not_Exists.mp4' is invalid or "
        "does not exist."
    )
    assert str(error.value) == expected_error


def test_media_path_with_image():
    with pytest.raises(TypeError) as error:
        _Media(test_files[4])
    expected_error = (
        "Invalid file type: Expected a video or audio file, got image file "
        "instead."
    )
    assert str(error.value) == expected_error


def test_media_path_with_video():
    media = _Media(test_files[2])
    assert isinstance(media, _Media)


def test_media_path_with_audio():
    media = _Media(test_files[3])
    assert isinstance(media, _Media)
