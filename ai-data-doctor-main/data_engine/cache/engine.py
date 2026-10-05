from .config import (
    CACHE_ENABLED
)

from .file_hash import (
    generate_file_hash
)

from .cache_manager import (

    save_to_cache,

    load_from_cache,

    delete_cache,

    clear_all_cache,

    is_cache_expired
)


def get_cached_result(
    file_path
):

    """
    Check whether results
    already exist in cache.
    """

    if not CACHE_ENABLED:

        return None

    cache_key = generate_file_hash(
        file_path
    )

    cache_data = load_from_cache(
        cache_key
    )

    if cache_data is None:

        return None

    if is_cache_expired(
        cache_data
    ):

        delete_cache(
            cache_key
        )

        return None

    return {

        "cache_key":
            cache_key,

        "data":
            cache_data["data"],

        "cached":
            True
    }


def save_cached_result(
    file_path,
    result
):

    """
    Save pipeline result.
    """

    if not CACHE_ENABLED:

        return None

    cache_key = generate_file_hash(
        file_path
    )

    cache_path = save_to_cache(
        cache_key,
        result
    )

    return {

        "cache_key":
            cache_key,

        "cache_path":
            cache_path,

        "cached":
            True
    }


def clear_cache():

    """
    Clear complete cache.
    """

    return clear_all_cache()