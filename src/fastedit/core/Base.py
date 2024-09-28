import os
import shutil
from tempfile import TemporaryDirectory
from fastedit.core.utils import _guess_file_type

class _Base:
    def __init__(
        self,
        path: str
    ):
        """
        Initializes an instance of base with the specified path.

        Parameters
        ----------
        path: str
            Path to the file.

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