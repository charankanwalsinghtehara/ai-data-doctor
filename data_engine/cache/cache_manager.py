import pickle

from pathlib import Path

from datetime import datetime

from .config import (
    CACHE_DIRECTORY_NAME,
    CACHE_FILE_EXTENSION,
    MAX_CACHE_AGE_HOURS
)


def get_cache_directory():

    """
    Get project cache directory.
    """

    base_directory = (
        Path(__file__)
        .resolve()
        .parent
        .parent
        .parent
    )

    cache_directory = (

        base_directory
        / CACHE_DIRECTORY_NAME
    )

    cache_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return cache_directory


def get_cache_path(
    cache_key
):

    cache_directory = (
        get_cache_directory()
    )

    return (

        cache_directory
        / f"{cache_key}{CACHE_FILE_EXTENSION}"
    )


def save_to_cache(
    cache_key,
    data
):

    """
    Save data into cache.
    """

    cache_path = get_cache_path(
        cache_key
    )

    cache_data = {

        "created_at":
            datetime.now(),

        "data":
            data
    }

    with open(
        cache_path,
        "wb"
    ) as file:

        pickle.dump(
            cache_data,
            file
        )

    return str(
        cache_path
    )


def load_from_cache(
    cache_key
):

    """
    Load cached data.
    """

    cache_path = get_cache_path(
        cache_key
    )

    if not cache_path.exists():

        return None

    with open(
        cache_path,
        "rb"
    ) as file:

        cache_data = pickle.load(
            file
        )

    return cache_data


def delete_cache(
    cache_key
):

    """
    Delete one cache file.
    """

    cache_path = get_cache_path(
        cache_key
    )

    if cache_path.exists():

        cache_path.unlink()

        return True

    return False


def clear_all_cache():

    """
    Delete all cache files.
    """

    cache_directory = (
        get_cache_directory()
    )

    count = 0

    for cache_file in cache_directory.glob(
        f"*{CACHE_FILE_EXTENSION}"
    ):

        cache_file.unlink()

        count += 1

    return count


def is_cache_expired(
    cache_data
):

    """
    Check whether cache
    is too old.
    """

    if cache_data is None:

        return True

    created_at = cache_data.get(
        "created_at"
    )

    if created_at is None:

        return True

    age = (

        datetime.now()
        - created_at
    )

    age_hours = (

        age.total_seconds()
        / 3600
    )

    return age_hours > MAX_CACHE_AGE_HOURS


