TARGET_KEYWORDS = [
    "target",
    "label",
    "class",
    "outcome",
    "result",
    "status",
    "prediction",
    "churn",
    "default",
    "fraud",
    "survived"
]


def calculate_target_score(column_name, series):

    score = 0

    name = str(column_name).lower()

    for keyword in TARGET_KEYWORDS:

        if keyword in name:
            score += 50

    # A target usually should not have
    # a unique value for every row.
    non_null = series.dropna()

    if len(non_null) > 0:

        unique_ratio = (
            non_null.nunique()
            / len(non_null)
        )

        if unique_ratio < 0.5:
            score += 20

    return score


def detect_target_column(dataframe):
    """
    Return possible ML target columns.
    """

    candidates = []

    for column in dataframe.columns:

        score = calculate_target_score(
            column,
            dataframe[column]
        )

        if score > 0:

            candidates.append({
                "column": column,
                "confidence_score": score
            })

    candidates.sort(
        key=lambda item:
            item["confidence_score"],
        reverse=True
    )

    return candidates