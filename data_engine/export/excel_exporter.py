from .exceptions import (
    ExportError
)


def export_excel(
    dataframe,
    output_directory,
    filename="cleaned_dataset.xlsx"
):
    """
    Export DataFrame as Excel.
    """

    try:

        file_path = (
            output_directory
            / filename
        )

        dataframe.to_excel(
            file_path,
            index=False
        )

        return str(file_path)

    except Exception as error:

        raise ExportError(
            f"Excel export failed: {error}"
        )