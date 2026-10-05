from pathlib import Path

import joblib


def save_model(
    model,
    model_name,
    save_directory="saved_models"
):
    """
    Save trained ML model.
    """

    save_path = Path(
        save_directory
    )

    save_path.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = (
        save_path /
        f"{model_name}.joblib"
    )

    joblib.dump(
        model,
        file_path
    )

    return str(file_path)


def load_model(
    file_path
):
    """
    Load a saved ML model.
    """

    return joblib.load(
        file_path
    )