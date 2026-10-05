import pandas as pd


def analyze_categorical_numerical(
    dataframe,
    understanding_result
):
    """
    Analyze categorical vs numerical relationships.
    """

    results = {}

    categorical_columns = []

    numerical_columns = []

    for column, information in (
        understanding_result["columns"]
        .items()
    ):

        role = information.get("role")

        if role == "categorical":

            categorical_columns.append(
                column
            )

        elif role == "numerical":

            numerical_columns.append(
                column
            )

    for categorical_column in categorical_columns:

        for numerical_column in numerical_columns:

            if (
                categorical_column
                not in dataframe.columns
                or numerical_column
                not in dataframe.columns
            ):

                continue

            grouped_data = (
                dataframe
                .groupby(categorical_column)[
                    numerical_column
                ]
                .agg([
                    "count",
                    "mean",
                    "median",
                    "min",
                    "max"
                ])
            )

            if grouped_data.empty:

                continue

            results[
                f"{categorical_column}__{numerical_column}"
            ] = {

                "categorical_column":
                    categorical_column,

                "numerical_column":
                    numerical_column,

                "group_statistics":
                    grouped_data
                    .round(4)
                    .to_dict(
                        orient="index"
                    )
            }

    return results