import matplotlib.pyplot as plt

import numpy as np


def create_correlation_chart(
    dataframe,
    output_directory
):
    """
    Create correlation heatmap
    using Matplotlib only.
    """

    numeric_dataframe = (
        dataframe.select_dtypes(
            include="number"
        )
    )

    if numeric_dataframe.shape[1] < 2:

        return None

    correlation_matrix = (
        numeric_dataframe.corr()
    )

    plt.figure(
        figsize=(10, 8)
    )

    image = plt.imshow(
        correlation_matrix,
        aspect="auto"
    )

    plt.colorbar(image)

    plt.xticks(

        range(
            len(
                correlation_matrix.columns
            )
        ),

        correlation_matrix.columns,

        rotation=45,

        ha="right"
    )

    plt.yticks(

        range(
            len(
                correlation_matrix.columns
            )
        ),

        correlation_matrix.columns
    )

    plt.title(
        "Correlation Matrix"
    )

    plt.tight_layout()

    file_path = (
        output_directory
        / "correlation_matrix.png"
    )

    plt.savefig(
        file_path
    )

    plt.close()

    return str(file_path)