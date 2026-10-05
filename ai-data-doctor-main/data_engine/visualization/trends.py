import pandas as pd

import matplotlib.pyplot as plt


def find_datetime_columns(
    dataframe
):
    """
    Try to identify datetime columns.
    """

    datetime_columns = []

    for column in dataframe.columns:

        if (
            pd.api.types.is_datetime64_any_dtype(
                dataframe[column]
            )
        ):

            datetime_columns.append(
                column
            )

    return datetime_columns


def create_trend_charts(
    dataframe,
    output_directory,
    max_numeric_columns=5
):
    """
    Create trend charts
    when datetime columns exist.
    """

    generated_charts = []

    datetime_columns = (
        find_datetime_columns(
            dataframe
        )
    )

    numeric_columns = (

        dataframe.select_dtypes(
            include="number"
        )

        .columns

        .tolist()
    )

    if not datetime_columns:

        return generated_charts

    if not numeric_columns:

        return generated_charts

    date_column = datetime_columns[0]

    numeric_columns = (
        numeric_columns[
            :max_numeric_columns
        ]
    )

    sorted_dataframe = (
        dataframe.sort_values(
            by=date_column
        )
    )

    for numeric_column in numeric_columns:

        plt.figure(
            figsize=(10, 5)
        )

        plt.plot(

            sorted_dataframe[
                date_column
            ],

            sorted_dataframe[
                numeric_column
            ]
        )

        plt.title(
            f"{numeric_column} Over Time"
        )

        plt.xlabel(
            date_column
        )

        plt.ylabel(
            numeric_column
        )

        plt.xticks(
            rotation=45
        )

        plt.tight_layout()

        safe_name = (

            str(numeric_column)

            .replace(" ", "_")

            .replace("/", "_")
        )

        file_path = (

            output_directory

            / f"{safe_name}_trend.png"
        )

        plt.savefig(
            file_path
        )

        plt.close()

        generated_charts.append(
            str(file_path)
        )

    return generated_charts