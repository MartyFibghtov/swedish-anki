"""Module description."""

import os
import pathlib

from aqt import mw


def get_file_path(file_name) -> str:
    """Get filepath in AnkiFileSystem.

    Args:
        file_name: filename that needs to be saved.

    Returns:
        Path where file can be stored.
    """
    collection_path = pathlib.Path(mw.col.path).parent.absolute()
    media_path = os.path.join(collection_path, 'collection.media')

    return os.path.join(media_path, file_name)


def get_content_folder_path() -> str:
    """Get content folder path in AnkiFileSystem.

    Returns:
        Path where content can be saved.
    """
    collection_path = pathlib.Path(mw.col.path).parent.absolute()
    return os.path.join(collection_path, 'collection.media')


