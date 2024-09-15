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
