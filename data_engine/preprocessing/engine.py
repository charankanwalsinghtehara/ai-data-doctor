from .missing_handler import (
    handle_missing_values
)

from .encoder import (
    encode_categorical_columns
)

from .scaler import (
    scale_numeric_features
)


def run_preprocessing_engine(

    dataframe,

    scale_data=False
):
    """
    Run complete preprocessing
    pipeline.
    """

    # Keep original safe

    processed_dataframe = (

        dataframe.copy()
    )


    # =========================
    # HANDLE MISSING VALUES
    # =========================

    processed_dataframe = (

        handle_missing_values(
            processed_dataframe
        )
    )


    # =========================
    # ENCODE CATEGORIES
    # =========================

    processed_dataframe = (

        encode_categorical_columns(
            processed_dataframe
        )
    )


    # =========================
    # SCALE DATA
    # =========================

    if scale_data:

        processed_dataframe = (

            scale_numeric_features(
                processed_dataframe
            )
        )


    return processed_dataframe