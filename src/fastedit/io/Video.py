import ffmpeg
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
