import math
import ffmpeg
from typing import Union
from fastedit.core.Media import _Media
from fastedit.core.utils import _guess_file_type


class Video(_Media):
    def __init__(
        self,
        path: str
    ):
        """
        Initializes an instance of video with the specified path.

        Parameters
        ----------
        path: str
            Path to the video file.

        Raises
        ------
        TypeError
            If the specified path is not a str.
        """
        # Guess mime type
        file_mime_type = _guess_file_type(path)
        # Verifying that mime type is video
        if not file_mime_type == "video":
            raise TypeError(
                f"Invalid file type: Expected a video file, got "
                f"{file_mime_type} file instead."
            )
        # Initialize instance
        super().__init__(path)

    def resize(
        self,
        height: int,
        width: int
    ):
        """
        Resizes a video to the specified height and width.

        Parameters
        ----------
        height: int
            The desired height of the video in pixels (divisible by 2).
        width: int
            The desired width of the video in pixels (divisible by 2).

        Raises
        ------
        TypeError
            If height or width are not int.
        ValueError
            If height or width are not positive integer.
        ValueError
            If height or width are not divisible by 2.
        """
        # Verifying parameters types
        if not isinstance(height, int):
            raise TypeError(
                f"Expected 'height' to be of type 'int', but got "
                f"'{type(height).__name__}' instead."
            )
        if not isinstance(width, int):
            raise TypeError(
                f"Expected 'width' to be of type 'int', but got "
                f"'{type(width).__name__}' instead."
            )
        # Verifying parameters values
        if height <= 0 or width <= 0:
            raise ValueError(
                f"Invalid value: 'height' and 'width' must be positive "
                f"integers. Got height={height}, width={width}."
            )
        if height % 2 != 0 or width % 2 != 0:
            raise ValueError(
                f"Invalid value: 'height' and 'width' must be "
                f"divisible by 2. Got height={height} and width={width}."
            )
        # Resizing input video
        input = ffmpeg.input(
            filename=self._main_temp_file,
        )
        # Defining output and codec copying
        output = ffmpeg.output(
            input,
            self._second_temp_file,
            vf=f"scale={width}:{height}"
        )
        overwrite = ffmpeg.overwrite_output(
            output
        )
        # Running command
        ffmpeg.run(
            stream_spec=overwrite,
            quiet=True
        )
        # Saving result to main file
        self._move_and_replace()

    def crop(
        self,
        x: int,
        y: int,
        height: int,
        width: int
    ):
        """
        Crop the video to a specific rectangular area.

        Parameters
        ----------
        x: int
            The x-coordinate of the center of the crop area.
        y: int
            The y-coordinate of the center of the crop area.
        height: int
            The height of the crop area in pixels. Must be a positive integer.
        width: int
            The width of the crop area in pixels. Must be a positive integer.

        Raises
        ------
        TypeError
            If x, y, height, or width are not of type `int`.
        ValueError
            If the provided height or width are not positive integers.
        """
        # Verifying parameters types
        if not isinstance(x, int):
            raise TypeError(
                f"Expected 'x' to be of type 'int', but got "
                f"'{type(x).__name__}' instead."
            )
        if not isinstance(y, int):
            raise TypeError(
                f"Expected 'y' to be of type 'int', but got "
                f"'{type(y).__name__}' instead."
            )
        if not isinstance(height, int):
            raise TypeError(
                f"Expected 'height' to be of type 'int', but got "
                f"'{type(height).__name__}' instead."
            )
        if not isinstance(width, int):
            raise TypeError(
                f"Expected 'width' to be of type 'int', but got "
                f"'{type(width).__name__}' instead."
            )
        # Verifying parameters values
        if height <= 0 or width <= 0:
            raise ValueError(
                f"Invalid value: 'height' and 'width' must be positive "
                f"integers. Got height={height}, width={width}."
            )
        # Getting vertical and horizontal positions for FFmpeg
        cropped_x = x - (width/2)
        cropped_y = y - (height/2)
        # Input video
        input = ffmpeg.input(
            filename=self._main_temp_file
        )
        # Cropping video
        crop = ffmpeg.crop(
            stream=input,
            x=cropped_x,
            y=cropped_y,
            height=height,
            width=width
        )
        # Defining output and codec copying
        output = ffmpeg.output(
            crop,
            input.audio,
            self._second_temp_file,
            acodec="copy"
        )
        overwrite = ffmpeg.overwrite_output(
            output
        )
        # Running command
        ffmpeg.run(
            stream_spec=overwrite,
            quiet=True
        )
        # Saving result to main file
        self._move_and_replace()

    def _get_video_metadata(
        self
    ):
        """
        Gets only video's metadata.

        Returns
        -------
        video_metadata: dict
            Dictionary containing video's metadata.

        Raises
        ------
        ValueError
            If no video codec type is found.
        """
        metadata = self.metadata()
        video_metadata = next(
            (
                dictionary
                for dictionary in metadata["streams"]
                if dictionary.get("codec_type") == "video"
            ),
            None
        )
        if video_metadata is None:
            raise ValueError(
                "No dictionary with 'codec_type' == 'video' found."
            )
        return video_metadata

    def zoom_in(
        self,
        zoom: Union[int, float]
    ):
        """
        Applies a progressive zoom effect until the end of the video.

        Parameters
        ----------
        zoom: Union[int, float]
            The zoom factor to achieve at the end of the video. Range is 0-10.

        Raises
        ------
        TypeError
            If zoom is not of type `int` or `float`.
        ValueError
            If zoom is not greater than or equal to 0.
        """
        # Verifying parameters types
        if not isinstance(zoom, (int, float)):
            raise TypeError(
                f"Expected 'zoom' to be of type 'int' or 'float', but got "
                f"'{type(zoom).__name__}' instead."
            )
        # Verifying parameter value
        if zoom < 0:
            raise ValueError(
                f"Invalid value: 'zoom' must be greater than or equal to 0. "
                f"Got zoom={zoom}."
            )
        # Getting video metadata
        metadata = self._get_video_metadata()
        fps = math.ceil(eval(metadata["r_frame_rate"]))
        height = metadata["height"]
        width = metadata["width"]
        total_frames = int(metadata["nb_frames"])
        # Computing zoom factor
        zoom_factor = zoom/total_frames
        # Input video
        input = ffmpeg.input(
            filename=self._main_temp_file
        )

        # Zooming in video
        zoom = ffmpeg.zoompan(
            input,
            z=f"pzoom+{zoom_factor}",
            x="iw/2-(iw/zoom/2)",
            y="ih/2-(ih/zoom/2)",
            d=1,
            fps=fps,
            s=f"{width}x{height}"
        )
        # Defining output and codec copying
        output = ffmpeg.output(
            zoom,
            input.audio,
            self._second_temp_file
        )
        overwrite = ffmpeg.overwrite_output(
            output
        )
        # Running command
        ffmpeg.run(
            stream_spec=overwrite,
            quiet=True
        )
        # Saving result to main file
        self._move_and_replace()

    def text(
        self,
        x: int,
        y: int,
        text: str,
        start: Union[int, float],
        end: Union[int, float],
        fontfile: str = None,
        fontsize: int = 24,
        fontcolor: str = "white",
        borderw: int = 5,
        bordercolor: str = "black",
        box: bool = False,
        boxborderw: int = 5,
        boxcolor: str = "black"
    ):
        """
        Add text to the video at specific coordinates and duration.

        Parameters
        ----------
        x: int
            The x-coordinate for the text's position on the video.
        y: int
            The y-coordinate for the text's position on the video.
        text: str
            The content of the text to be rendered on the video.
        start: int or float
            The start time (in seconds) from when the text will appear on the
            video.
        end: int or float
            The end time (in seconds) when the text will disappear from the
            video.
        fontfile: str, optional
            The path to the font file to be used for the text. Default is
            None.
        fontsize: int, optional
            The font size to be used for the text. Default is 24.
        fontcolor: str, optional
            The color of the text. Default is "white". The set of possible
            values at https://ffmpeg.org/ffmpeg-utils.html#color-syntax.
        borderw: int, optional
            The width of the border around the text. Default is 5.
        bordercolor: str, optional
            The color of the border around the text. Default is "black". The
            set of possible values at
            https://ffmpeg.org/ffmpeg-utils.html#color-syntax.
        box: bool, optional
            Whether to draw a box around the text using the background color.
            Default is False.
        boxborderw: int, optional
            The width of the border around the box. Default is 5.
        boxcolor: str, optional
            The color of the box around the text. Default is "black". The set
            of possible values at
            https://ffmpeg.org/ffmpeg-utils.html#color-syntax.

        Raises
        ------
        TypeError
            If `x` is not an int.
            If `y` is not an int.
            If `text` is not a str.
            If `start` is not an int or float.
            If `end` is not an int or float.
        ValueError
            If `end` is not strictly greater than `start`.
            If `end` is strictly greater than media duration.
        """
        # Verifying parameters types
        if not isinstance(x, int):
            raise TypeError(
                f"Expected 'x' to be of type 'int', but got "
                f"'{type(x).__name__}' instead."
            )
        if not isinstance(y, int):
            raise TypeError(
                f"Expected 'y' to be of type 'int', but got "
                f"'{type(y).__name__}' instead."
            )
        if not isinstance(text, str):
            raise TypeError(
                f"Expected 'text' to be of type 'str', but got "
                f"'{type(text).__name__}' instead."
            )
        if not isinstance(start, (int, float)):
            raise TypeError(
                f"Expected 'start' to be of type 'int' or 'float', but got "
                f"'{type(start).__name__}' instead."
            )
        if not isinstance(end, (int, float)):
            raise TypeError(
                f"Expected 'end' to be of type 'int' or 'float', but got "
                f"'{type(end).__name__}' instead."
            )
        # Verifying parameters consistency
        if not end > start:
            raise ValueError(
                f"Invalid 'end' value: 'end' must be strictly greater than "
                f"'start'. Got start={start} and end={end}."
            )
        metadata = self.metadata()
        media_duration = float(metadata["duration"])
        if not end <= media_duration:
            raise ValueError(
                f"Invalid 'end' value: 'end' must be less than or equal to "
                f"the media duration. Got end={end}, but media duration is "
                f"{media_duration}."
            )
        # Boolean to 0 | 1
        box_enabled = int(box)
        # Input video
        input = ffmpeg.input(
            filename=self._main_temp_file
        )
        # Text in video
        zoom = ffmpeg.drawtext(
            input,
            x=f"{x}-(text_w)/2",
            y=f"{y}-(text_h)/2",
            text=text,
            enable=f"between(t,{start},{end})",
            fontfile=fontfile,
            fontsize=fontsize,
            fontcolor=fontcolor,
            borderw=borderw,
            bordercolor=bordercolor,
            box=box_enabled,
            boxborderw=boxborderw,
            boxcolor=boxcolor
        )
        # Defining output and codec copying
        output = ffmpeg.output(
            zoom,
            input.audio,
            self._second_temp_file
        )
        overwrite = ffmpeg.overwrite_output(
            output
        )
        # Running command
        ffmpeg.run(
            stream_spec=overwrite,
            quiet=True
        )
        # Saving result to main file
        self._move_and_replace()
