from fastedit.io.Audio import Audio
import ffmpeg
import pytest
import os


test_files = [
    "./media/test_audio.mp3",
    "./media/test_video_with_audio.mp4"
]


def test_audio_path_with_audio():
    audio = Audio(test_files[0])
    assert isinstance(audio, Audio)


def test_audio_path_with_video():
    with pytest.raises(TypeError) as error:
        Audio(test_files[1])
    expected_error = (
        "Invalid file type: Expected a audio file, got video file instead."
    )
    assert str(error.value) == expected_error


def test_audio_metadata_with_ffprobe():
    audio = Audio(test_files[0])
    output = audio.metadata()
    assert len(output) == 6
    assert output["format_name"] == "mp3"
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "mp3"


def test_audio_metadata_without_ffprobe(monkeypatch):
    # Mocking FFprobe not installed
    def mock_ffprobe(*args, **kwargs):
        raise ffmpeg.Error(
            "ffprobe",
            "stdout",
            "stderr"
        )

    # Replace ffmpeg.probe by mocking
    monkeypatch.setattr(ffmpeg, "probe", mock_ffprobe)

    # Testing
    audio = Audio(test_files[0])
    with pytest.raises(ffmpeg.Error) as error:
        audio.metadata()
    expected_error = (
        "ffprobe error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_audio_clip_int_int():
    audio = Audio(test_files[0])
    audio.clip(
        start=0,
        end=10
    )
    output = audio.metadata()
    assert output["format_name"] == "mp3"
    assert int(float(output["duration"])) == 10
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "mp3"


def test_audio_clip_int_float():
    audio = Audio(test_files[0])
    audio.clip(
        start=0,
        end=10.1
    )
    output = audio.metadata()
    assert output["format_name"] == "mp3"
    assert int(float(output["duration"])) == 10
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "mp3"


def test_audio_clip_float_int():
    audio = Audio(test_files[0])
    audio.clip(
        start=0.1,
        end=10
    )
    output = audio.metadata()
    assert output["format_name"] == "mp3"
    assert int(float(output["duration"])) == 9
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "mp3"


def test_audio_clip_float_float():
    audio = Audio(test_files[0])
    audio.clip(
        start=0.1,
        end=10.2
    )
    output = audio.metadata()
    assert output["format_name"] == "mp3"
    assert int(float(output["duration"])) == 10
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "mp3"


def test_audio_clip_start_greater_than_end():
    audio = Audio(test_files[0])
    with pytest.raises(ValueError) as error:
        audio.clip(
            start=10,
            end=0
        )
    expected_error = (
        "Invalid 'end' value: 'end' must be strictly greater than "
        "'start'. Got start=10 and end=0."
    )
    assert str(error.value) == expected_error


def test_audio_clip_start_and_end_greater_than_video_duration():
    audio = Audio(test_files[0])
    metadata = audio.metadata()
    audio_duration = float(metadata["duration"])
    with pytest.raises(ValueError) as error:
        audio.clip(
            start=20,
            end=35
        )
    expected_error = (
        "Invalid 'end' value: 'end' must be less than or equal to "
        "the media duration. Got end=35, but media duration is "
        f"{audio_duration}."
    )
    assert str(error.value) == expected_error


def test_audio_clip_without_ffmpeg(monkeypatch):
    # Mocking FFmpeg not installed
    def mock_ffmpeg(*args, **kwargs):
        raise ffmpeg.Error(
            "ffmpeg",
            "stdout",
            "stderr"
        )

    # Replace ffmpeg.run by mocking
    monkeypatch.setattr(ffmpeg, "run", mock_ffmpeg)

    # Testing
    audio = Audio(test_files[0])
    with pytest.raises(ffmpeg.Error) as error:
        audio.clip(
            start=0,
            end=10
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_audio_loop_int():
    audio = Audio(test_files[0])
    audio.loop(
        duration=35
    )
    output = audio.metadata()
    assert output["format_name"] == "mp3"
    assert int(float(output["duration"])) == 35
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "mp3"


def test_audio_loop_float():
    audio = Audio(test_files[0])
    audio.loop(
        duration=35.4
    )
    output = audio.metadata()
    assert output["format_name"] == "mp3"
    assert int(float(output["duration"])) == 35
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "mp3"


def test_audio_loop_without_ffmpeg(monkeypatch):
    # Mocking FFmpeg not installed
    def mock_ffmpeg(*args, **kwargs):
        raise ffmpeg.Error(
            "ffmpeg",
            "stdout",
            "stderr"
        )

    # Replace ffmpeg.run by mocking
    monkeypatch.setattr(ffmpeg, "run", mock_ffmpeg)

    # Testing
    audio = Audio(test_files[0])
    with pytest.raises(ffmpeg.Error) as error:
        audio.loop(
            duration=35
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_audio_save_valid_path():
    audio = Audio(test_files[0])
    save_path = "test_fastedit.mp3"
    audio.save(
        path=save_path
    )
    assert os.path.exists(save_path)


def test_audio_save_invalid_path():
    audio = Audio(test_files[0])
    save_path = "path/to/save/file.mp3"
    with pytest.raises(ValueError) as error:
        audio.save(
            path=save_path
        )
    expected_error = (
        f"The specified path '{save_path}' is invalid or does not exist."
    )
    assert str(error.value) == expected_error


def test_audio_save_wrong_path_type():
    audio = Audio(test_files[0])
    save_path = 1
    with pytest.raises(TypeError) as error:
        audio.save(
            path=save_path
        )
    expected_error = (
        "Expected 'path' to be of type 'str', but got "
        "'int' instead."
    )
    assert str(error.value) == expected_error
