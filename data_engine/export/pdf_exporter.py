# pyright: reportMissingModuleSource=false

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    PageBreak
)

from reportlab.lib.units import (
    inch
)

from .exceptions import (
    ExportError
)


def format_value(
    value
):
    """
    Convert values into readable text.
    """

    if isinstance(
        value,
        dict
    ):

        lines = []

        for key, item in value.items():

            lines.append(
                f"{key}: {format_value(item)}"
            )

        return "<br/>".join(
            lines
        )

    if isinstance(
        value,
        list
    ):

        return "<br/>".join(

            format_value(item)

            for item in value
        )

    return str(value)


def add_section(
    story,
    title,
    content,
    styles
):
    """
    Add a report section.
    """

    story.append(

        Paragraph(

            title,

            styles["Heading2"]
        )
    )

    story.append(

        Spacer(
            1,
            0.15 * inch
        )
    )

    formatted_content = (
        format_value(content)
    )

    story.append(

        Paragraph(

            formatted_content,

            styles["BodyText"]
        )
    )

    story.append(

        Spacer(
            1,
            0.25 * inch
        )
    )


def export_pdf(
    report,
    output_directory,
    filename="data_doctor_report.pdf"
):
    """
    Generate AI Data Doctor PDF report.
    """

    try:

        file_path = (
            output_directory
            / filename
        )

        document = SimpleDocTemplate(

            str(file_path),

            pagesize=A4
        )

        styles = (
            getSampleStyleSheet()
        )

        story = []

        # TITLE

        story.append(

            Paragraph(

                "AI DATA DOCTOR REPORT",

                styles["Title"]
            )
        )

        story.append(

            Spacer(
                1,
                0.3 * inch
            )
        )

        # REPORT INFORMATION

        if "report_information" in report:

            add_section(

                story,

                "Report Information",

                report[
                    "report_information"
                ],

                styles
            )

        # DATASET

        if "dataset" in report:

            add_section(

                story,

                "Dataset Overview",

                report[
                    "dataset"
                ],

                styles
            )

        # DATA QUALITY

        if "data_quality" in report:

            add_section(

                story,

                "Data Quality",

                report[
                    "data_quality"
                ],

                styles
            )

        # CLEANING

        if "cleaning" in report:

            add_section(

                story,

                "Data Cleaning",

                report[
                    "cleaning"
                ],

                styles
            )

        # ANALYSIS

        if "analysis" in report:

            add_section(

                story,

                "Data Analysis",

                report[
                    "analysis"
                ],

                styles
            )

        # ANOMALIES

        if "anomalies" in report:

            add_section(

                story,

                "Anomaly Detection",

                report[
                    "anomalies"
                ],

                styles
            )

        # MACHINE LEARNING

        if "machine_learning" in report:

            add_section(

                story,

                "Machine Learning",

                report[
                    "machine_learning"
                ],

                styles
            )

        # RECOMMENDATIONS

        if "final_recommendations" in report:

            add_section(

                story,

                "Final Recommendations",

                report[
                    "final_recommendations"
                ],

                styles
            )

        document.build(
            story
        )

        return str(file_path)

    except Exception as error:

        raise ExportError(
            f"PDF export failed: {error}"
        )