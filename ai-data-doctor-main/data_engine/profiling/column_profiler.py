import pandas as pd


def get_basic_column_profile(series):
    """
    Generate basic information for one column.
    """

    total_rows = len(series)

    missing_count = int(
        series.isna().sum()
    )

    non_missing_count = (
        total_rows - missing_count
    )

    if total_rows > 0:

        missing_percentage = round(
            (missing_count / total_rows) * 100,
            2
        )

    else:

        missing_percentage = 0

    return {
        "name": str(series.name),

        "pandas_dtype":
            str(series.dtype),

        "total_values":
            int(total_rows),

        "non_missing_values":
            int(non_missing_count),

        "missing_values":
            int(missing_count),

        "missing_percentage":
            missing_percentage,

        "unique_values":
            int(series.nunique())
    }


def get_column_sample(series, sample_size=5):
    """
    Get example values from a column.
    """

    values = (
        series.dropna()
        .head(sample_size)
        .tolist()
    )

    samples = []

    for value in values:

        if hasattr(value, "item"):

            value = value.item()

        samples.append(str(value))

    return samples


def profile_columns(
    dataframe,
    understanding_result
):
    """
    Create profiles for every column.
    """

    results = {}

    understanding_columns = (
        understanding_result["columns"]
    )

    for column in dataframe.columns:

        series = dataframe[column]

        basic_profile = (
            get_basic_column_profile(
                series
            )
        )

        samples = get_column_sample(
            series
        )

        understanding = (
            understanding_columns.get(
                column,
                {}
            )
        )

        results[column] = {
            "basic": basic_profile,

            "samples": samples,

            "understanding": {
                "technical_type":
                    understanding.get(
                        "technical_type"
                    ),

                "role":
                    understanding.get(
                        "role"
                    ),

                "semantic_type":
                    understanding.get(
                        "semantic_type"
                    )
            }
        }

    return results