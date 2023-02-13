"""Module to download files."""

from datetime import datetime
import requests


def download_url_to_file(
    url: str,
    where_to_save: str,
    add_time_prefix: bool = True,
) -> str:
    """Download from url to file.

    Args:
        url: Url to file online
        where_to_save: where to save new file
        add_time_prefix: add time prefix to files so that files are unique

    Returns:
        file_path

    Raises:
        ValueError: if any of parameters are empty.
    """
    if not url:
        raise ValueError('Empty or null url')
    if not where_to_save:
        raise ValueError('Empty or null file_path')

    file_name = url.split('/')[-1]
    if add_time_prefix:
        file_name = str(datetime.now()) + file_name

    file_path = '{0}{1}'.format(where_to_save, file_name)

    response = requests.get(url=url)

    with open(file_path, 'wb') as content_file:
        content_file.write(response.content)

    return file_name
