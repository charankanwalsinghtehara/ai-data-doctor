import pandas as pd


def interpret_correlation(value):
    """
    Convert correlation value into
    human-readable interpretation.
    """

    absolute_value = abs(value)

    if absolute_value >= 0.9:
        strength = "very_strong"

    elif absolute_value >= 0.7:
        strength = "strong"

    elif absolute_value >= 0.5:
        strength = "moderate"

    elif absolute_value >= 0.3:
        strength = "weak"

    else:
        strength = "very_weak"

    if value > 0:
        direction = "positive"

    elif value < 0:
        direction = "negative"

    else:
        direction = "none"

    return {
        "strength": strength,
        "direction": direction
    }


def analyze_correlations(dataframe):
    """
    Analyze correlations between numerical columns.
    """

    numerical_dataframe = (
        dataframe.select_dtypes(
            include="number"
        )
    )

    if numerical_dataframe.shape[1] < 2:

        return {
            "available": False,
            "message":
                "At least two numerical columns are required.",
            "matrix": {},
            "relationships": []
        }

    correlation_matrix = (
        numerical_dataframe.corr()
    )

    relationships = []

    columns = correlation_matrix.columns.tolist()

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            column_1 = columns[i]
            column_2 = columns[j]

            correlation_value = (
                correlation_matrix.loc[
                    column_1,
                    column_2
                ]
            )

            if pd.isna(correlation_value):
                continue

            interpretation = (
                interpret_correlation(
                    float(correlation_value)
                )
            )

            relationships.append({

                "column_1": column_1,

                "column_2": column_2,

                "correlation":
                    round(
                        float(correlation_value),
                        4
                    ),

                "strength":
                    interpretation["strength"],

                "direction":
                    interpretation["direction"]
            })

    relationships.sort(
        key=lambda item:
        abs(item["correlation"]),
        reverse=True
    )

    return {

        "available": True,

        "matrix":
            correlation_matrix
            .round(4)
            .to_dict(),

        "relationships":
            relationships
    }