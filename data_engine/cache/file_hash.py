import hashlib


def generate_file_hash(
    file_path,
    chunk_size=8192
):
    """
    Generate SHA256 hash
    for a file.
    """

    hasher = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as file:

        while True:

            chunk = file.read(
                chunk_size
            )

            if not chunk:

                break

            hasher.update(
                chunk
            )

    return hasher.hexdigest()