import matplotlib.pyplot as plt


def create_missing_values_chart(
    dataframe,
    output_directory
):
    """
    Create missing values bar chart.
    """

    missing_values = (
        dataframe.isnull()
        .sum()
    )

    missing_values = (
        missing_values[
            missing_values > 0
        ]
    )

    if missing_values.empty:

        return None

    plt.figure(
        figsize=(10, 6)
    )

    missing_values.plot(
        kind="bar"
    )

    plt.title(
        "Missing Values by Column"
    )

    plt.xlabel(
        "Columns"
    )

    plt.ylabel(
        "Missing Values"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    file_path = (
        output_directory
        / "missing_values.png"
    )

    plt.savefig(
        file_path
    )

    plt.close()

    return str(file_path)