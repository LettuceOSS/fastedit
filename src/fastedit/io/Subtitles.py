from fastedit.core.Base import _Base
from fastedit.core.utils import _guess_file_type
import ffmpeg
import os


class Subtitles(_Base):
    def __init__(
        self,
        path: str
    ):
        """
        Initializes an instance of subtitles with the specified path.

        Parameters
        ----------
        path: str
            Path to the subtitles file.

        Raises
        ------
        TypeError
            If the specified path is not a str.
        ValueError
            If the specified path is invalid or does not exist.
        """
        # Guess mime type
        file_mime_type = _guess_file_type(path)
        # Verifying that mime type is subtitles
        if not file_mime_type == "subtitles":
            raise TypeError(
                f"Invalid file type: Expected a subtitles file, got "
                f"{file_mime_type} file instead."
            )
        # Initialize instance
        super().__init__(path)
        self._change_to_ass()

    def _change_to_ass(
        self
    ):
        """
        Change subtitles format to ASS.
        """
        extension = ".ass"
        # Changing second temp file format
        self._second_temp_file = os.path.join(
            self._temp_dir.name,
            "second" + extension
        )
        # Changing subtitles format
        input = ffmpeg.input(
            filename=self._main_temp_file
        )
        output = ffmpeg.output(
            input,
            self._second_temp_file
        )
        # Overwrite output file
        overwrite = ffmpeg.overwrite_output(
            output
        )
        # Running command
        ffmpeg.run(
            stream_spec=overwrite,
            quiet=True
        )
        # Changing main temp file format
        self._main_temp_file = os.path.join(
            self._temp_dir.name,
            "main" + extension
        )
        # Saving result to main file
        self._move_and_replace()
