import pandas as pd


def calculate_target_score(
    series,
    column_name
):
    """
    Calculate how suitable a column is
    as a machine learning target.
    """

    score = 0

    total_rows = len(series)

    unique_count = series.nunique()

    missing_count = series.isna().sum()

    # Too many missing values
    if total_rows > 0:

        missing_ratio = (
            missing_count / total_rows
        )

        if missing_ratio < 0.2:

            score += 2

    # Not completely unique
    if unique_count < total_rows:

        score += 2

    # Column name hints
    column_name_lower = (
        column_name.lower()
    )

    target_keywords = [

        "target",
        "label",
        "class",
        "outcome",
        "result",
        "status",
        "price",
        "salary",
        "income",
        "sales",
        "score",
        "prediction"
    ]

    for keyword in target_keywords:

        if keyword in column_name_lower:

            score += 3

            break

    # Penalize likely ID columns
    id_keywords = [

        "id",
        "index",
        "serial",
        "code",
        "number"
    ]

    for keyword in id_keywords:

        if (
            column_name_lower == keyword
            or column_name_lower.endswith(
                f"_{keyword}"
            )
        ):

            score -= 5

            break

    return score


def detect_target_candidates(
    dataframe
):
    """
    Detect possible target columns.
    """

    candidates = []

    for column in dataframe.columns:

        series = dataframe[column]

        unique_count = (
            series.nunique()
        )

        total_rows = len(series)

        # Skip completely unique columns
        # unless numerical and meaningful
        if (
            unique_count == total_rows
            and not pd.api.types.is_numeric_dtype(
                series
            )
        ):

            continue

        score = calculate_target_score(
            series,
            column
        )

        candidates.append({

            "column": column,

            "score": score,

            "unique_values":
                int(unique_count),

            "dtype":
                str(series.dtype)
        })

    candidates.sort(

        key=lambda item:
        item["score"],

        reverse=True
    )

    return candidates


def get_recommended_targets(
    dataframe,
    top_n=5
):
    """
    Return the best target candidates.
    """

    candidates = (
        detect_target_candidates(
            dataframe
        )
    )

    return candidates[:top_n]