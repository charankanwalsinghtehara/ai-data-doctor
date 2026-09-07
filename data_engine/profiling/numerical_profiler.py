import pandas as pd


def safe_value(value):
    """
    Convert Pandas/Numpy values into normal Python values.
    """

    if pd.isna(value):
        return None

    if hasattr(value, "item"):
        return value.item()

    return value


def profile_numerical_column(series):
    """
    Generate detailed statistics for a numerical column.
    """

    non_null = series.dropna()

    if len(non_null) == 0:

        return {
            "count": 0,
            "mean": None,
            "median": None,
            "std": None,
            "variance": None,
            "min": None,
            "max": None,
            "q1": None,
            "q3": None,
            "range": None,
            "sum": None
        }

    minimum = non_null.min()
    maximum = non_null.max()

    return {
        "count": int(non_null.count()),

        "mean":
            safe_value(non_null.mean()),

        "median":
            safe_value(non_null.median()),

        "std":
            safe_value(non_null.std()),

        "variance":
            safe_value(non_null.var()),

        "min":
            safe_value(minimum),

        "max":
            safe_value(maximum),

        "q1":
            safe_value(
                non_null.quantile(0.25)
            ),

        "q3":
            safe_value(
                non_null.quantile(0.75)
            ),

        "range":
            safe_value(maximum - minimum),

        "sum":
            safe_value(non_null.sum())
    }


def profile_all_numerical_columns(dataframe):
    """
    Profile every numerical column.
    """

    results = {}

    numerical_columns = dataframe.select_dtypes(
        include="number"
    ).columns

    for column in numerical_columns:

        results[column] = profile_numerical_column(
            dataframe[column]
        )

    return results