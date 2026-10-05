import pandas as pd


def detect_trend(values):

    if len(values) < 2:

        return "insufficient_data"

    first_value = values.iloc[0]

    last_value = values.iloc[-1]

    if last_value > first_value:

        return "increasing"

    elif last_value < first_value:

        return "decreasing"

    return "stable"


def analyze_time_trends(
    dataframe,
    understanding_result
):
    """
    Analyze trends using datetime columns.
    """

    results = {}

    datetime_columns = []

    numerical_columns = (
        dataframe.select_dtypes(
            include="number"
        ).columns
        .tolist()
    )

    for column, information in (
        understanding_result["columns"]
        .items()
    ):

        semantic_type = (
            information.get(
                "semantic_type"
            )
        )

        if semantic_type == "datetime":

            datetime_columns.append(
                column
            )

    for date_column in datetime_columns:

        if date_column not in dataframe.columns:
            continue

        temporary_dataframe = dataframe.copy()

        temporary_dataframe[date_column] = (
            pd.to_datetime(
                temporary_dataframe[
                    date_column
                ],
                errors="coerce"
            )
        )

        temporary_dataframe = (
            temporary_dataframe
            .dropna(subset=[date_column])
            .sort_values(date_column)
        )

        if temporary_dataframe.empty:
            continue

        for numerical_column in numerical_columns:

            values = (
                temporary_dataframe[
                    numerical_column
                ]
            )

            trend = detect_trend(values)

            results[
                f"{date_column}__{numerical_column}"
            ] = {

                "date_column":
                    date_column,

                "numerical_column":
                    numerical_column,

                "trend":
                    trend,

                "first_value":
                    float(values.iloc[0]),

                "last_value":
                    float(values.iloc[-1])
            }

    return results