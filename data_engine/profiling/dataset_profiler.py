import pandas as pd


def profile_dataset(dataframe):
    """
    Generate overall dataset information.
    """

    rows, columns = dataframe.shape

    memory_bytes = dataframe.memory_usage(
        deep=True
    ).sum()

    memory_mb = round(
        memory_bytes / (1024 * 1024),
        4
    )

    return {
        "rows": int(rows),
        "columns": int(columns),
        "total_cells": int(rows * columns),
        "memory_usage_mb": memory_mb,
        "column_names": dataframe.columns.tolist(),
        "is_empty": bool(dataframe.empty)
    }