import os
import shutil
import ffmpeg
from typing import Union
from tempfile import TemporaryDirectory
from fastedit.core.utils import _guess_file_type


class _Media:
    def __init__(
        self,
        path: str
    ):
        """
        Initializes an instance of media with the specified path.

        Parameters
        ----------
        path: str
            Path to the media file.

        Raises
        ------
        TypeError
            If the specified path is not a str.
        ValueError
            If the specified path is invalid or does not exist.
        """
        # Verifying path's type
        if not isinstance(path, str):
            raise TypeError(
                f"Expected 'path' to be of type 'str', but got "
                f"'{type(path).__name__}' instead."
            )
        # Verifying if path exists
        if not os.path.exists(path):
            raise ValueError(
                f"The specified path '{path}' is invalid or does not exist."
            )
        # Verifying media mimetype
        file_mime_type = _guess_file_type(path)
        if file_mime_type not in ["video", "audio"]:
            raise TypeError(
                f"Invalid file type: Expected a video or audio file, got "
                f"{file_mime_type} file instead."
            )
        # Creating a temp directory for intermediate results
        cwd = os.getcwd()
        self._temp_dir = TemporaryDirectory(
            dir=cwd,
            prefix="fastedit-temp-dir"
        )
        # Defining temporary files
        extension = os.path.splitext(path)[1]
        self._main_temp_file = os.path.join(
            self._temp_dir.name,
            "main" + extension
        )
        self._second_temp_file = os.path.join(
            self._temp_dir.name,
            "second" + extension
        )
        # Copying source file into the main temporary file
        shutil.copy(
            path,
            self._main_temp_file
        )

    def __refactor_ffprobe_data(
        self,
        ffprobe_metadata: dict
    ):
        """
        Filters and refactors FFprobe metadata.

        Parameters
        ----------
        ffprobe_metadata: dict
            Dictionary containing FFprobe metadata.

        Returns
        -------
        ffprobe_metadata_refactored: dict
            Dictionary containing refactored media's metadata.

        Raises
        ------
        TypeError
            If ffprobe_metadata is not a dict.
        """
        # Verifying FFprobe's metadata type
        if not isinstance(ffprobe_metadata, dict):
            raise TypeError(
                f"Expected 'ffprobe_metadata' to be of type 'dict', but got "
                f"'{type(ffprobe_metadata).__name__}' instead."
            )
        # Selecting and refactoring format metadata
        format_data = ffprobe_metadata["format"]
        format_data_to_keep = [
            "format_name",
            "start_time",
            "duration",
            "size",
            "bit_rate"
        ]
        format_existing_keys = list(format_data.keys())
        ffprobe_metadata_refactored = {
            key: format_data[key]
            for key in format_data_to_keep
            if key in format_existing_keys
        }
        # Selecting and refactoring streams metadata
        streams_data = ffprobe_metadata["streams"]
        streams_data_to_keep = [
            "codec_type",
            "codec_name",
            "width",
            "height",
            "coded_width",
            "coded_height",
            "display_aspect_ratio",
            "pix_fmt",
            "duration",
            "bit_rate",
            "nb_frames",
            "sample_rate",
            "channels",
            "channel_layout",
            "r_frame_rate"
        ]
        streams_refactored = []
        for stream in streams_data:
            streams_existing_keys = list(stream.keys())
            stream_filtered = {
                key: stream[key]
                for key in streams_data_to_keep
                if key in streams_existing_keys
            }
            streams_refactored.append(
                stream_filtered
            )
        # Aggregating metadata in one dict
        ffprobe_metadata_refactored["streams"] = streams_refactored
        return ffprobe_metadata_refactored

    def metadata(
        self
    ):
        """
        Gather metadata about the media.

        Returns
        -------
        media_metadata: dict
            Dictionary containing media's metadata.
        """
        ffprobe_metadata = ffmpeg.probe(
            filename=self._main_temp_file
        )
        media_metadata = self.__refactor_ffprobe_data(ffprobe_metadata)
        return media_metadata

    def _move_and_replace(
        self
    ):
        """
        Moving second file to main file
        """
        shutil.move(
            src=self._second_temp_file,
            dst=self._main_temp_file
        )

    def clip(
        self,
        start: Union[int, float],
        end: Union[int, float]
    ):
        """
        Extracts a portion of the media.

        Parameters
        ----------
        start: float
            Start time of the clip in seconds.
        end: float
            End time of the clip in seconds.

        Raises
        ------
        TypeError
            If start or end are not int or float.
        ValueError
            If end is not strictly greater than start.
        ValueError
            If end is strictly greater than media duration.
        """
        # Verifying parameters types
        if not isinstance(start, (float, int)):
            raise TypeError(
                f"Expected 'start' to be of type 'float' or 'int', but got "
                f"'{type(start).__name__}' instead."
            )
        if not isinstance(end, (float, int)):
            raise TypeError(
                f"Expected 'end' to be of type 'float' or 'int', but got "
                f"'{type(start).__name__}' instead."
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
        # Trimming input media
        input = ffmpeg.input(
            filename=self._main_temp_file,
            ss=start,
            to=end
        )
        # Defining output and codec copying
        output = ffmpeg.output(
            input,
            self._second_temp_file,
            c="copy"
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

    def loop(
        self,
        duration: Union[int, float]
    ):
        """
        Loops a media over a specified time period.

        Parameters
        ----------
        duration: int or float
            The duration, in seconds, for which the media will loop.

        Raises
        ------
        TypeError
            If duration is not int or float.
        """
        # Verifying parameters types
        if not isinstance(duration, (float, int)):
            raise TypeError(
                f"Expected 'duration' to be of type 'float' or 'int', but got "
                f"'{type(duration).__name__}' instead."
            )
        # Looping input media
        input = ffmpeg.input(
            filename=self._main_temp_file,
            stream_loop="-1",
            t=duration
        )
        # Defining output and codec copying
        output = ffmpeg.output(
            input,
            self._second_temp_file,
            c="copy"
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

    def save(
        self,
        path: str
    ):
        """
        Saves the media file to the specified path in the filesystem.

        Parameters
        ----------
        path : str
            The destination file path where the media file will be saved.

        Raises
        ------
        TypeError
            If `path` is not of type `str`.
        ValueError
            If the specified `path` is invalid or does not exist.
        """
        # Verifying path's type
        if not isinstance(path, str):
            raise TypeError(
                f"Expected 'path' to be of type 'str', but got "
                f"'{type(path).__name__}' instead."
            )
        # Verifying if path exists
        media_abs_path = os.path.abspath(
            path=path
        )
        media_dir_path = os.path.dirname(
            p=media_abs_path
        )
        if not os.path.exists(media_dir_path):
            raise ValueError(
                f"The specified path '{path}' is invalid or does not exist."
            )
        # Copying file to filesystem
        shutil.copy(
            self._main_temp_file,
            path
        )
