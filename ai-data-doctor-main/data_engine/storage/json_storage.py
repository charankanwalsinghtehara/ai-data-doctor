import json

from pathlib import Path

import numpy as np

import pandas as pd

from datetime import datetime


def convert_to_json_serializable(
    value
):
    """
    Convert Python, NumPy and Pandas
    objects into JSON-safe values.
    """

    if isinstance(
        value,
        dict
    ):

        return {

            str(key):
            convert_to_json_serializable(
                item
            )

            for key, item
            in value.items()
        }

    if isinstance(
        value,
        list
    ):

        return [

            convert_to_json_serializable(
                item
            )

            for item
            in value
        ]

    if isinstance(
        value,
        tuple
    ):

        return [

            convert_to_json_serializable(
                item
            )

            for item
            in value
        ]

    if isinstance(
        value,
        np.integer
    ):

        return int(value)

    if isinstance(
        value,
        np.floating
    ):

        return float(value)

    if isinstance(
        value,
        np.ndarray
    ):

        return value.tolist()

    if isinstance(
        value,
        pd.Timestamp
    ):

        return value.isoformat()

    if isinstance(
        value,
        datetime
    ):

        return value.isoformat()

    if pd.isna(value):

        return None

    return value


def save_json(
    data,
    file_path
):
    """
    Save data as JSON.
    """

    file_path = Path(
        file_path
    )

    file_path.parent.mkdir(

        parents=True,

        exist_ok=True
    )

    serializable_data = (
        convert_to_json_serializable(
            data
        )
    )

    with open(

        file_path,

        "w",

        encoding="utf-8"

    ) as file:

        json.dump(

            serializable_data,

            file,

            indent=4,

            ensure_ascii=False
        )

    return str(file_path)


def load_json(
    file_path
):
    """
    Load JSON data.
    """

    file_path = Path(
        file_path
    )

    if not file_path.exists():

        return None

    with open(

        file_path,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(file)