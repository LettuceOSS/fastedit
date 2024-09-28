from fastedit.io.Subtitles import Subtitles
import pytest


test_files = [
    "./media/test_subtitles.srt",
    "./media/This_File_Does_Not_Exists.srt",
    "./media/test_video_with_audio.mp4",
    1
]


def test_subtitles_with_valid_file():
    subtitles = Subtitles(test_files[0])
    assert isinstance(subtitles, Subtitles)


def test_subtitles_with_invalid_file():
    with pytest.raises(ValueError) as error:
        Subtitles(test_files[1])
    expected_error = (
        f"The specified path '{test_files[1]}' does not exist or is not "
        "a file."
    )
    assert str(error.value) == expected_error


def test_subtitles_with_invalid_format():
    with pytest.raises(TypeError) as error:
        Subtitles(test_files[2])
    expected_error = (
        "Invalid file type: Expected a subtitles file, got "
        "video file instead."
    )
    assert str(error.value) == expected_error


def test_subtitles_with_invalid_type():
    with pytest.raises(TypeError) as error:
        Subtitles(test_files[3])
    expected_error = (
        "Expected 'path' to be of type 'str', but got "
        "'int' instead."
    )
    assert str(error.value) == expected_error
