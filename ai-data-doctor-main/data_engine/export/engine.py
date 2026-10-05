import pandas as pd

from .exceptions import (
    ExportError
)

from .paths import (
    get_export_directory
)

from .csv_exporter import (
    export_csv
)

from .excel_exporter import (
    export_excel
)

from .json_exporter import (
    export_json
)

from .pdf_exporter import (
    export_pdf
)

from .project_zipper import (
    export_project_zip
)


def run_export_engine(

    project_id,

    cleaned_dataframe=None,

    final_report=None,

    export_csv_file=True,

    export_excel_file=True,

    export_json_file=True,

    export_pdf_file=True,

    export_zip_file=True
):
    """
    Run complete export pipeline.
    """

    output_directory = (
        get_export_directory(
            project_id
        )
    )

    results = {

        "project_id":
            project_id,

        "exports": {}
    }

    # -------------------------
    # CSV
    # -------------------------

    if (

        export_csv_file

        and

        cleaned_dataframe is not None
    ):

        path = export_csv(

            cleaned_dataframe,

            output_directory
        )

        results["exports"][
            "csv"
        ] = path

    # -------------------------
    # EXCEL
    # -------------------------

    if (

        export_excel_file

        and

        cleaned_dataframe is not None
    ):

        path = export_excel(

            cleaned_dataframe,

            output_directory
        )

        results["exports"][
            "excel"
        ] = path

    # -------------------------
    # JSON REPORT
    # -------------------------

    if (

        export_json_file

        and

        final_report is not None
    ):

        path = export_json(

            final_report,

            output_directory
        )

        results["exports"][
            "json"
        ] = path

    # -------------------------
    # PDF REPORT
    # -------------------------

    if (

        export_pdf_file

        and

        final_report is not None
    ):

        path = export_pdf(

            final_report,

            output_directory
        )

        results["exports"][
            "pdf"
        ] = path

    # -------------------------
    # COMPLETE ZIP
    # -------------------------

    if export_zip_file:

        path = export_project_zip(

            project_id,

            output_directory
        )

        results["exports"][
            "zip"
        ] = path

    results["total_exports"] = (

        len(
            results["exports"]
        )
    )

    return results