from pathlib import Path

import pandas as pd

from .paths import (
    get_dataset_directory
)


def save_original_dataset(
    dataframe,
    project_id
):
    """
    Save original dataset.
    """

    dataset_directory = (
        get_dataset_directory(
            project_id
        )
    )

    dataset_directory.mkdir(

        parents=True,

        exist_ok=True
    )

    file_path = (
        dataset_directory
        / "original.csv"
    )

    dataframe.to_csv(

        file_path,

        index=False
    )

    return str(file_path)


def save_cleaned_dataset(
    dataframe,
    project_id
):
    """
    Save cleaned dataset.
    """

    dataset_directory = (
        get_dataset_directory(
            project_id
        )
    )

    dataset_directory.mkdir(

        parents=True,

        exist_ok=True
    )

    file_path = (
        dataset_directory
        / "cleaned.csv"
    )

    dataframe.to_csv(

        file_path,

        index=False
    )

    return str(file_path)


def load_original_dataset(
    project_id
):
    """
    Load original dataset.
    """

    file_path = (

        get_dataset_directory(
            project_id
        )

        / "original.csv"
    )

    if not file_path.exists():

        return None

    return pd.read_csv(
        file_path
    )


def load_cleaned_dataset(
    project_id
):
    """
    Load cleaned dataset.
    """

    file_path = (

        get_dataset_directory(
            project_id
        )

        / "cleaned.csv"
    )

    if not file_path.exists():

        return None

    return pd.read_csv(
        file_path
    )