from .exceptions import (
    ExportError
)


def export_csv(
    dataframe,
    output_directory,
    filename="cleaned_dataset.csv"
):
    """
    Export DataFrame as CSV.
    """

    try:

        file_path = (
            output_directory
            / filename
        )

        dataframe.to_csv(
            file_path,
            index=False
        )

        return str(file_path)

    except Exception as error:

        raise ExportError(
            f"CSV export failed: {error}"
        )