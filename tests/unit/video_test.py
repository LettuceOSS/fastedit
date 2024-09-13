from fastedit.io.Video import Video
import ffmpeg
import pytest


test_files = [
    "./media/test_video_with_audio.mp4",
    "./media/test_audio.mp3"
]


def test_video_path_with_video():
    video = Video(test_files[0])
    assert isinstance(video, Video)


def test_video_path_with_audio():
    with pytest.raises(TypeError) as error:
        Video(test_files[1])
    expected_error = (
        "Invalid file type: Expected a video file, got audio file instead."
    )
    assert str(error.value) == expected_error


def test_video_metadata_with_ffprobe():
    video = Video(test_files[0])
    output = video.metadata()
    assert len(output) == 6
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"


def test_video_metadata_without_ffprobe(monkeypatch):
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
    video = Video(test_files[0])
    with pytest.raises(ffmpeg.Error) as error:
        video.metadata()
    expected_error = (
        "ffprobe error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error

def test_video_cut():
    video = Video(test_files[0])
    video.clip(
        start=0,
        end=10
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 10
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"

def test_video_cut_without_ffmpeg(monkeypatch):
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
    video = Video(test_files[0])
    with pytest.raises(ffmpeg.Error) as error:
        video.clip(
            start=0,
            end=10
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error
