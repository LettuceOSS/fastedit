from fastedit.core.Base import _Base
from fastedit.core.utils import _guess_file_type


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