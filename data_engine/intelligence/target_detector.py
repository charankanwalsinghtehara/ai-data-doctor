import pandas as pd


TARGET_KEYWORDS = [

    "target",

    "label",

    "class",

    "outcome",

    "result",

    "prediction",

    "status",

    "approved",

    "default",

    "fraud",

    "churn",

    "survived",

    "diagnosis"
]


def detect_target_candidates(
    dataframe
):
    """
    Detect possible ML target columns.
    """

    candidates = []


    for column in dataframe.columns:

        column_name = str(
            column
        ).lower()


        # =========================
        # KEYWORD MATCH
        # =========================

        keyword_match = any(

            keyword in column_name

            for keyword in TARGET_KEYWORDS
        )


        unique_count = (

            dataframe[column]
            .nunique(
                dropna=True
            )
        )


        total_rows = len(
            dataframe
        )


        if total_rows == 0:

            continue


        unique_ratio = (

            unique_count
            / total_rows
        )


        # =========================
        # SCORE
        # =========================

        score = 0


        if keyword_match:

            score += 50


        # Categorical columns
        # with limited unique values
        # are possible targets

        if unique_count <= 20:

            score += 20


        if unique_ratio < 0.5:

            score += 10


        if pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):

            score += 5


        if score > 0:

            candidates.append({

                "column":
                    str(column),

                "score":
                    score,

                "unique_values":
                    int(unique_count)
            })


    candidates = sorted(

        candidates,

        key=lambda item:
            item["score"],

        reverse=True
    )


    return candidates