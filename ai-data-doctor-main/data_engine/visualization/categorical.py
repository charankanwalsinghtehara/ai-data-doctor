import matplotlib.pyplot as plt


def create_categorical_charts(
    dataframe,
    output_directory,
    max_columns=10
):
    """
    Create count charts
    for categorical columns.
    """

    generated_charts = []

    categorical_columns = (

        dataframe.select_dtypes(
            include=[
                "object",
                "category"
            ]
        )

        .columns

        .tolist()
    )

    categorical_columns = (
        categorical_columns[
            :max_columns
        ]
    )

    for column in categorical_columns:

        value_counts = (

            dataframe[column]

            .astype(str)

            .value_counts()

            .head(15)
        )

        if value_counts.empty:

            continue

        plt.figure(
            figsize=(10, 6)
        )

        value_counts.plot(
            kind="bar"
        )

        plt.title(
            f"Top Categories in {column}"
        )

        plt.xlabel(
            column
        )

        plt.ylabel(
            "Count"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        safe_name = (

            str(column)

            .replace(" ", "_")

            .replace("/", "_")
        )

        file_path = (

            output_directory

            / f"{safe_name}_categories.png"
        )

        plt.savefig(
            file_path
        )

        plt.close()

        generated_charts.append(
            str(file_path)
        )

    return generated_charts