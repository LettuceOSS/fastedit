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
    expected_output = {
        'format_name': 'mov,mp4,m4a,3gp,3g2,mj2',
        'start_time': '0.000000',
        'duration': '15.627007',
        'size': '11916526',
        'bit_rate': '6100477',
        'streams': [
            {
                'codec_type': 'video',
                'codec_name': 'h264',
                'width': 1920,
                'height': 1080,
                'coded_width': 1920,
                'coded_height': 1080,
                'display_aspect_ratio': '16:9',
                'pix_fmt': 'yuv420p',
                'duration': '15.482133',
                'bit_rate': '6021118',
                'nb_frames': '464'
            },
            {
                'codec_type': 'audio',
                'codec_name': 'aac',
                'duration': '15.627007',
                'bit_rate': '125611',
                'nb_frames': '674',
                'sample_rate': '44100',
                'channels': 2,
                'channel_layout': 'stereo'
            }
        ]
    }
    assert output == expected_output


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
