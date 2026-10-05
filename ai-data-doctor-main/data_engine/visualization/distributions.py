import matplotlib.pyplot as plt

import pandas as pd


def create_distribution_charts(
    dataframe,
    output_directory,
    max_columns=10
):
    """
    Create distribution charts
    for numeric columns.
    """

    generated_charts = []

    numeric_columns = (
        dataframe.select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    numeric_columns = (
        numeric_columns[
            :max_columns
        ]
    )

    for column in numeric_columns:

        data = (
            dataframe[column]
            .dropna()
        )

        if data.empty:

            continue

        plt.figure(
            figsize=(8, 5)
        )

        plt.hist(
            data,
            bins=30
        )

        plt.title(
            f"Distribution of {column}"
        )

        plt.xlabel(
            column
        )

        plt.ylabel(
            "Frequency"
        )

        plt.tight_layout()

        safe_name = (
            str(column)
            .replace(" ", "_")
            .replace("/", "_")
        )

        file_path = (

            output_directory

            / f"{safe_name}_distribution.png"
        )

        plt.savefig(
            file_path
        )

        plt.close()

        generated_charts.append(
            str(file_path)
        )

    return generated_charts