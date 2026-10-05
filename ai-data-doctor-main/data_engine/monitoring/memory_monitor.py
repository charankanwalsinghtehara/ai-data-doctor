import os

import psutil


def get_memory_usage():
    """
    Get current Python process
    memory usage.
    """

    process = psutil.Process(
        os.getpid()
    )


    memory_info = process.memory_info()


    memory_bytes = memory_info.rss


    memory_mb = (

        memory_bytes
        / (1024 * 1024)
    )


    return {

        "memory_bytes":

            memory_bytes,

        "memory_mb":

            round(
                memory_mb,
                2
            )
    }


def get_memory_difference(
    before_memory,
    after_memory
):
    """
    Calculate memory difference.
    """

    before_mb = before_memory[
        "memory_mb"
    ]

    after_mb = after_memory[
        "memory_mb"
    ]


    difference = (

        after_mb
        - before_mb
    )


    return {

        "before_memory_mb":
            before_mb,

        "after_memory_mb":
            after_mb,

        "memory_difference_mb":
            round(
                difference,
                2
            )
    }