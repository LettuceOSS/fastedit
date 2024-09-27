from fastedit.io.Video import Video
from fastedit.io.Audio import Audio
import ffmpeg
import pytest
import os


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


def test_video_clip_int_int():
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


def test_video_clip_int_float():
    video = Video(test_files[0])
    video.clip(
        start=0,
        end=10.1
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 10
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"


def test_video_clip_float_int():
    video = Video(test_files[0])
    video.clip(
        start=0.1,
        end=10
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 10
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"


def test_video_clip_float_float():
    video = Video(test_files[0])
    video.clip(
        start=0.1,
        end=10.2
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 10
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"


def test_video_clip_start_greater_than_end():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.clip(
            start=10,
            end=0
        )
    expected_error = (
        "Invalid 'end' value: 'end' must be strictly greater than "
        "'start'. Got start=10 and end=0."
    )
    assert str(error.value) == expected_error


def test_video_clip_start_and_end_greater_than_video_duration():
    video = Video(test_files[0])
    metadata = video.metadata()
    video_duration = float(metadata["duration"])
    with pytest.raises(ValueError) as error:
        video.clip(
            start=20,
            end=25
        )
    expected_error = (
        "Invalid 'end' value: 'end' must be less than or equal to "
        "the media duration. Got end=25, but media duration is "
        f"{video_duration}."
    )
    assert str(error.value) == expected_error


def test_video_clip_without_ffmpeg(monkeypatch):
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


def test_video_loop_int():
    video = Video(test_files[0])
    video.loop(
        duration=20
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 20
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"


def test_video_loop_float():
    video = Video(test_files[0])
    video.loop(
        duration=21.4
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 21
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"


def test_video_loop_without_ffmpeg(monkeypatch):
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
        video.loop(
            duration=20
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_resize_float_int():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.resize(
            height=426.1,
            width=240
        )
    expected_error = (
        "Expected 'height' to be of type 'int', but got "
        "'float' instead."
    )
    assert str(error.value) == expected_error


def test_video_resize_int_float():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.resize(
            height=426,
            width=240.1
        )
    expected_error = (
        "Expected 'width' to be of type 'int', but got "
        "'float' instead."
    )
    assert str(error.value) == expected_error


def test_video_resize_float_float():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.resize(
            height=426.1,
            width=240.1
        )
    expected_error = (
        "Expected 'height' to be of type 'int', but got "
        "'float' instead."
    )
    assert str(error.value) == expected_error


def test_video_resize_negative_positive():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.resize(
            height=-426,
            width=240
        )
    expected_error = (
        "Invalid value: 'height' and 'width' must be positive integers. Got "
        "height=-426, width=240."
    )
    assert str(error.value) == expected_error


def test_video_resize_positive_negative():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.resize(
            height=426,
            width=-240
        )
    expected_error = (
        "Invalid value: 'height' and 'width' must be positive integers. Got "
        "height=426, width=-240."
    )
    assert str(error.value) == expected_error


def test_video_resize_negative_negative():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.resize(
            height=-426,
            width=-240
        )
    expected_error = (
        "Invalid value: 'height' and 'width' must be positive integers. Got "
        "height=-426, width=-240."
    )
    assert str(error.value) == expected_error


def test_video_resize_positive_positive():
    video = Video(test_files[0])
    video.resize(
        height=426,
        width=240
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"
    assert output["streams"][0]["height"] == 426
    assert output["streams"][0]["width"] == 240


def test_video_resize_not_divisible_by_2():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.resize(
            height=427,
            width=241
        )
    expected_error = (
        "Invalid value: 'height' and 'width' must be "
        "divisible by 2. Got height=427 and width=241."
    )
    assert str(error.value) == expected_error


def test_video_resize_without_ffmpeg(monkeypatch):
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
        video.resize(
            height=426,
            width=240
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_crop_all_int():
    video = Video(test_files[0])
    video.crop(
        x=960,
        y=540,
        height=480,
        width=640
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"
    assert output["streams"][0]["height"] == 480
    assert output["streams"][0]["width"] == 640


def test_video_crop_x_not_int():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.crop(
            x=960.1,
            y=540,
            height=480,
            width=640
        )
    expected_error = (
        "Expected 'x' to be of type 'int', but got "
        "'float' instead."
    )
    assert str(error.value) == expected_error


def test_video_crop_y_not_int():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.crop(
            x=960,
            y=540.1,
            height=480,
            width=640
        )
    expected_error = (
        "Expected 'y' to be of type 'int', but got "
        "'float' instead."
    )
    assert str(error.value) == expected_error


def test_video_crop_height_not_int():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.crop(
            x=960,
            y=540,
            height=480.1,
            width=640
        )
    expected_error = (
        "Expected 'height' to be of type 'int', but got "
        "'float' instead."
    )
    assert str(error.value) == expected_error


def test_video_crop_width_not_int():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.crop(
            x=960,
            y=540,
            height=480,
            width=640.1
        )
    expected_error = (
        "Expected 'width' to be of type 'int', but got "
        "'float' instead."
    )
    assert str(error.value) == expected_error


def test_video_crop_width_negative():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.crop(
            x=960,
            y=540,
            height=480,
            width=-1
        )
    expected_error = (
        "Invalid value: 'height' and 'width' must be positive "
        "integers. Got height=480, width=-1."
    )
    assert str(error.value) == expected_error


def test_video_crop_height_negative():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.crop(
            x=960,
            y=540,
            height=-1,
            width=640
        )
    expected_error = (
        "Invalid value: 'height' and 'width' must be positive "
        "integers. Got height=-1, width=640."
    )
    assert str(error.value) == expected_error


def test_video_crop_without_ffmpeg(monkeypatch):
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
        video.crop(
            x=960,
            y=540,
            height=480,
            width=640
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_zoom_in_not_int_or_float_parameter():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.zoom_in(
            zoom="test"
        )
    expected_error = (
        "Expected 'zoom' to be of type 'int' or 'float', but got "
        "'str' instead."
    )
    assert str(error.value) == expected_error


def test_video_zoom_in_negative_parameter():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.zoom_in(
            zoom=-1
        )
    expected_error = (
        "Invalid value: 'zoom' must be greater than or equal to 0. "
        "Got zoom=-1."
    )
    assert str(error.value) == expected_error


def test_video_zoom_in_int_parameter():
    video = Video(test_files[0])
    video.zoom_in(
        zoom=1
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"
    assert output["streams"][0]["height"] == 1080
    assert output["streams"][0]["width"] == 1920


def test_video_zoom_in_float_parameter():
    video = Video(test_files[0])
    video.zoom_in(
        zoom=1.1
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"
    assert output["streams"][0]["height"] == 1080
    assert output["streams"][0]["width"] == 1920


def test_video_zoom_in_without_ffmpeg(monkeypatch):
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
        video.zoom_in(
            zoom=1.1
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_text_x_not_int():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.text(
            x="test",
            y=540,
            text="This is a text",
            start=0,
            end=10
        )
    expected_error = (
        "Expected 'x' to be of type 'int', but got "
        "'str' instead."
    )
    assert str(error.value) == expected_error


def test_video_text_y_not_int():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.text(
            x=960,
            y="test",
            text="This is a text",
            start=0,
            end=10
        )
    expected_error = (
        "Expected 'y' to be of type 'int', but got "
        "'str' instead."
    )
    assert str(error.value) == expected_error


def test_video_text_text_not_str():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.text(
            x=960,
            y=540,
            text=3,
            start=0,
            end=10
        )
    expected_error = (
        "Expected 'text' to be of type 'str', but got "
        "'int' instead."
    )
    assert str(error.value) == expected_error


def test_video_text_start_not_int_or_float():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.text(
            x=960,
            y=540,
            text="This is a text",
            start="test",
            end=10
        )
    expected_error = (
        "Expected 'start' to be of type 'int' or 'float', but got "
        "'str' instead."
    )
    assert str(error.value) == expected_error


def test_video_text_end_not_int_or_float():
    video = Video(test_files[0])
    with pytest.raises(TypeError) as error:
        video.text(
            x=960,
            y=540,
            text="This is a text",
            start=0,
            end="test"
        )
    expected_error = (
        "Expected 'end' to be of type 'int' or 'float', but got "
        "'str' instead."
    )
    assert str(error.value) == expected_error


def test_video_text_without_ffmpeg(monkeypatch):
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
        video.text(
            x=960,
            y=540,
            text="This is a text",
            start=0,
            end=10
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_text_start_greater_than_end():
    video = Video(test_files[0])
    with pytest.raises(ValueError) as error:
        video.text(
            x=960,
            y=540,
            text="This is a text",
            start=10,
            end=0
        )
    expected_error = (
        "Invalid 'end' value: 'end' must be strictly greater than "
        "'start'. Got start=10 and end=0."
    )
    assert str(error.value) == expected_error


def test_video_text_start_and_end_greater_than_video_duration():
    video = Video(test_files[0])
    metadata = video.metadata()
    video_duration = float(metadata["duration"])
    with pytest.raises(ValueError) as error:
        video.text(
            x=960,
            y=540,
            text="This is a text",
            start=0,
            end=20
        )
    expected_error = (
        "Invalid 'end' value: 'end' must be less than or equal to "
        "the media duration. Got end=20, but media duration is "
        f"{video_duration}."
    )
    assert str(error.value) == expected_error


def test_video_text_working():
    video = Video(test_files[0])
    video.text(
        x=960,
        y=540,
        text="This is a text",
        start=0,
        end=10
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"
    assert output["streams"][0]["height"] == 1080
    assert output["streams"][0]["width"] == 1920


def test_video_add_audio_wrong_audio_type_parameter():
    video = Video(test_files[0])
    audio = "test"
    with pytest.raises(TypeError) as error:
        video.add_audio(
            audio=audio,
            strategy="replace"
        )
    expected_error = (
        "Expected 'audio' to be of type 'Audio', but got "
        "'str' instead."
    )
    assert str(error.value) == expected_error


def test_video_add_audio_wrong_strategy_type_parameter():
    video = Video(test_files[0])
    audio = Audio(test_files[1])
    with pytest.raises(TypeError) as error:
        video.add_audio(
            audio=audio,
            strategy=1
        )
    expected_error = (
        "Expected 'strategy' to be of type 'str', but got "
        "'int' instead."
    )
    assert str(error.value) == expected_error


def test_video_add_audio_strategy_not_valid():
    video = Video(test_files[0])
    audio = Audio(test_files[1])
    with pytest.raises(ValueError) as error:
        video.add_audio(
            audio=audio,
            strategy="strat1"
        )
    expected_error = (
        "Invalid strategy 'strat1'. Expected one of: "
        "replace, add, mix."
    )
    assert str(error.value) == expected_error


def test_video_add_audio_replace_strategy():
    video = Video(test_files[0])
    audio = Audio(test_files[1])
    video.add_audio(
        audio=audio,
        strategy="replace"
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 2
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"
    assert output["streams"][0]["height"] == 1080
    assert output["streams"][0]["width"] == 1920


def test_video_add_audio_add_strategy():
    video = Video(test_files[0])
    audio = Audio(test_files[1])
    video.add_audio(
        audio=audio,
        strategy="add"
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 3
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][1]["codec_name"] == "aac"
    assert output["streams"][0]["height"] == 1080
    assert output["streams"][0]["width"] == 1920


def test_video_add_audio_mix_strategy():
    video = Video(test_files[0])
    audio = Audio(test_files[1])
    video.add_audio(
        audio=audio,
        strategy="mix"
    )
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 2
    assert output["streams"][1]["codec_name"] == "h264"
    assert output["streams"][0]["codec_name"] == "aac"
    assert output["streams"][1]["height"] == 1080
    assert output["streams"][1]["width"] == 1920


def test_video_add_audio_mix_strategy_without_ffmpeg(monkeypatch):
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
    audio = Audio(test_files[1])
    with pytest.raises(ffmpeg.Error) as error:
        video.add_audio(
            audio=audio,
            strategy="mix"
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_add_audio_replace_strategy_without_ffmpeg(monkeypatch):
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
    audio = Audio(test_files[1])
    with pytest.raises(ffmpeg.Error) as error:
        video.add_audio(
            audio=audio,
            strategy="replace"
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_add_audio_add_strategy_without_ffmpeg(monkeypatch):
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
    audio = Audio(test_files[1])
    with pytest.raises(ffmpeg.Error) as error:
        video.add_audio(
            audio=audio,
            strategy="add"
        )
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_remove_audio():
    video = Video(test_files[0])
    video.remove_audio()
    output = video.metadata()
    assert output["format_name"] == "mov,mp4,m4a,3gp,3g2,mj2"
    assert int(float(output["duration"])) == 15
    assert len(output["streams"]) == 1
    assert output["streams"][0]["codec_name"] == "h264"
    assert output["streams"][0]["height"] == 1080
    assert output["streams"][0]["width"] == 1920


def test_video_remove_audio_without_ffmpeg(monkeypatch):
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
        video.remove_audio()
    expected_error = (
        "ffmpeg error (see stderr output for detail)"
    )
    assert str(error.value) == expected_error


def test_video_save_valid_path():
    video = Video(test_files[0])
    save_path = ".venv/test.mp4"
    video.save(
        path=save_path
    )
    assert os.path.exists(save_path)


def test_video_save_invalid_path():
    video = Video(test_files[0])
    save_path = "path/to/save/file.mp4"
    with pytest.raises(ValueError) as error:
        video.save(
            path=save_path
        )
    expected_error = (
        f"The specified path '{save_path}' is invalid or does not exist."
    )
    assert str(error.value) == expected_error


def test_video_save_wrong_path_type():
    video = Video(test_files[0])
    save_path = 1
    with pytest.raises(TypeError) as error:
        video.save(
            path=save_path
        )
    expected_error = (
        "Expected 'path' to be of type 'str', but got "
        "'int' instead."
    )
    assert str(error.value) == expected_error
