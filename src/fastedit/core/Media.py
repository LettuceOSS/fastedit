import os
import shutil
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
        path : str
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
                f"Expected 'path' to be of type 'str', but got '{type(path).__name__}' instead."
            )
        # Verifying if path exists
        if not os.path.exists(path):
            raise ValueError(
                f"The specified path '{path}' is invalid or does not exist."
            )
        # Verifying media mimetype
        file_mime_type = _guess_file_type(path)
        if not file_mime_type in ["video", "audio"]:
            raise TypeError(f"Invalid file type: Expected a video or audio file, got {file_mime_type} file instead.")
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
