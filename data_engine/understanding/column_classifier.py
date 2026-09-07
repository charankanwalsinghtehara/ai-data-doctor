import pandas as pd


def get_non_null_series(series):
    """
    Return the column without missing values.
    """

    return series.dropna()


def is_identifier(series):
    """
    Check whether a column is likely an identifier.
    """

    column_name = str(series.name).lower()

    identifier_keywords = [
        "id",
        "uuid",
        "identifier",
        "customer_id",
        "user_id",
        "employee_id",
        "product_id",
        "order_id"
    ]

    if (
        column_name in identifier_keywords
        or column_name.endswith("_id")
    ):
        return True

    non_null = get_non_null_series(series)

    if len(non_null) == 0:
        return False

    unique_ratio = (
        non_null.nunique()
        / len(non_null)
    )

    # Highly unique string columns may be IDs.
    if (
        unique_ratio > 0.98
        and not pd.api.types.is_float_dtype(series)
    ):
        return True

    return False


def classify_column(series):
    """
    Classify the general role of one column.
    """

    non_null = get_non_null_series(series)

    if len(non_null) == 0:
        return "empty"

    if is_identifier(series):
        return "identifier"

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numerical"

    unique_count = non_null.nunique()

    unique_ratio = unique_count / len(non_null)

    # Small number of repeated values.
    if unique_count <= 20:
        return "categorical"

    # Repeated text values can still be categories.
    if unique_ratio < 0.5:
        return "categorical"

    return "text"


def classify_all_columns(dataframe):
    """
    Classify every column in the dataset.
    """

    results = {}

    for column in dataframe.columns:

        results[column] = classify_column(
            dataframe[column]
        )

    return results