from fastedit.core.utils import _guess_file_type
import pytest

test_files = [
    1,
    "This_File_Does_Not_Exists.mp4",
    "./media/test_video_with_audio.mp4",
    "./media/test_audio.mp3",
    "./media/test_image.jpeg",
    "./media/test_subtitles.srt"
]

def test_guess_file_type_with_number():
    with pytest.raises(TypeError) as error :
        _guess_file_type(test_files[0])
    assert str(error.value) == "Expected 'path' to be of type 'str', but got 'int' instead."

def test_guess_file_type_with_does_not_exists():
    with pytest.raises(ValueError) as error :
        _guess_file_type(test_files[1])
    assert str(error.value) == "The specified path 'This_File_Does_Not_Exists.mp4' does not exist or is not a file."

def test_guess_file_type_with_video():
    mimetype = _guess_file_type(test_files[2])
    assert mimetype == "video"

def test_guess_file_type_with_audio():
    mimetype = _guess_file_type(test_files[3])
    assert mimetype == "audio"

def test_guess_file_type_with_image():
    mimetype = _guess_file_type(test_files[4])
    assert mimetype == "image"

def test_guess_file_type_with_srt():
    mimetype = _guess_file_type(test_files[5])
    assert mimetype == None