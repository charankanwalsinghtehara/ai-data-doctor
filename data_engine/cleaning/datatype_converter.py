import pandas as pd


def convert_to_datetime(
    dataframe,
    column
):
    """
    Convert one column to datetime.
    """

    original_dtype = str(
        dataframe[column].dtype
    )

    converted = pd.to_datetime(
        dataframe[column],
        errors="coerce"
    )

    dataframe[column] = converted

    new_dtype = str(
        dataframe[column].dtype
    )

    failed_conversions = int(
        converted.isna().sum()
    )

    return {
        "original_dtype": original_dtype,
        "new_dtype": new_dtype,
        "failed_conversions":
            failed_conversions
    }


def convert_detected_datatypes(
    dataframe,
    understanding_result
):
    """
    Convert columns based on semantic detection.
    """

    cleaned_dataframe = dataframe.copy()

    results = {}

    for column in cleaned_dataframe.columns:

        column_info = (
            understanding_result["columns"]
            .get(column, {})
        )

        semantic_type = (
            column_info.get(
                "semantic_type"
            )
        )

        if semantic_type == "datetime":

            result = convert_to_datetime(
                cleaned_dataframe,
                column
            )

            results[column] = result

    return cleaned_dataframe, results