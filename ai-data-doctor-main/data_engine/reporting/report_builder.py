from datetime import datetime


def build_final_report(
    dataset_report,
    quality_report,
    cleaning_report,
    analysis_report,
    anomaly_report,
    ml_report,
    recommendations
):
    """
    Combine every report section.
    """

    return {

        "report_information": {

            "generated_at":
                datetime.now()
                .isoformat(),

            "system":
                "AI Data Doctor",

            "version":
                "1.0.0"
        },

        "dataset":
            dataset_report,

        "data_quality":
            quality_report,

        "cleaning":
            cleaning_report,

        "analysis":
            analysis_report,

        "anomalies":
            anomaly_report,

        "machine_learning":
            ml_report,

        "final_recommendations":
            recommendations
    }