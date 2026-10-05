import pandas as pd


def detect_column_data_type(series):
    """
    Detect the technical data type of a column.
    """

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_integer_dtype(series):
        return "integer"

    if pd.api.types.is_float_dtype(series):
        return "float"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    return "object"


def detect_dataframe_data_types(dataframe):
    """
    Detect technical data types for all columns.
    """

    results = {}

    for column in dataframe.columns:

        results[column] = detect_column_data_type(
            dataframe[column]
        )

    return results