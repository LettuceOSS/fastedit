from mimetypes import guess_type
import mimetypes
from os.path import isfile


def _guess_file_type(
    path: str
):
    """
    Guess the file type based on the file extension of the given path.

    Parameters
    ----------
    path: str
        The path to the file whose type needs to be determined. This should be
        a valid file path as a string.

    Raises
    ------
    TypeError
        If the specified path is not a str.
    ValueError
        If the specified path is not a file.
    """
    # Adding custom mimetypes
    mimetypes.add_type(
        type="subtitles/srt",
        ext=".srt"
    )
    mimetypes.add_type(
        type="subtitles/ass",
        ext=".ass"
    )
    # Verifying path's type
    if not isinstance(path, str):
        raise TypeError(
            f"Expected 'path' to be of type 'str', but got "
            f"'{type(path).__name__}' instead."
        )
    # Verifying existence
    if not isfile(path):
        raise ValueError(
            f"The specified path '{path}' does not exist or is not a file."
        )
    mime_type, _ = guess_type(path)
    if not isinstance(mime_type, str):
        return None
    if mime_type.startswith("video"):
        return "video"
    elif mime_type.startswith("image"):
        return "image"
    elif mime_type.startswith("audio"):
        return "audio"
    elif mime_type.startswith("subtitles"):
        return "subtitles"
    else:
        return None
