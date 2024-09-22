from fastedit.core.Media import _Media
from fastedit.core.utils import _guess_file_type


class Audio(_Media):
    def __init__(
        self,
        path: str
    ):
        """
        Initializes an instance of audio with the specified path.

        Parameters
        ----------
        path: str
            Path to the audio file.

        Raises
        ------
        TypeError
            If the file is not an audio.
        """
        # Guess mime type
        file_mime_type = _guess_file_type(path)
        # Verifying that mime type is audio
        if not file_mime_type == "audio":
            raise TypeError(
                f"Invalid file type: Expected a audio file, got "
                f"{file_mime_type} file instead."
            )
        # Initialize instance
        super().__init__(path)
