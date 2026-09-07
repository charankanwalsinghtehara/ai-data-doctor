import matplotlib.pyplot as plt


def create_outlier_charts(
    dataframe,
    output_directory,
    max_columns=10
):
    """
    Create boxplots
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

        plt.boxplot(
            data
        )

        plt.title(
            f"Outlier Analysis: {column}"
        )

        plt.ylabel(
            column
        )

        plt.tight_layout()

        safe_name = (

            str(column)

            .replace(" ", "_")

            .replace("/", "_")
        )

        file_path = (

            output_directory

            / f"{safe_name}_boxplot.png"
        )

        plt.savefig(
            file_path
        )

        plt.close()

        generated_charts.append(
            str(file_path)
        )

    return generated_charts