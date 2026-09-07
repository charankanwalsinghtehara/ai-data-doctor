from .dataset_report import (
    build_dataset_report
)

from .quality_report import (
    build_quality_report
)

from .cleaning_report import (
    build_cleaning_report
)

from .analysis_report import (
    build_analysis_report
)

from .anomaly_report import (
    build_anomaly_report
)

from .ml_report import (
    build_ml_report
)

from .recommendation_engine import (
    generate_final_recommendations
)

from .report_builder import (
    build_final_report
)


def generate_report(

    dataframe,

    understanding_result=None,

    profiling_result=None,

    quality_result=None,

    cleaning_result=None,

    analysis_result=None,

    anomaly_result=None,

    ml_recommendations=None,

    ml_result=None
):
    """
    Generate complete AI Data Doctor report.
    """

    # Dataset
    dataset_report = (
        build_dataset_report(

            dataframe,

            understanding_result,

            profiling_result
        )
    )

    # Quality
    quality_report = (
        build_quality_report(
            quality_result
        )
    )

    # Cleaning
    cleaning_report = (
        build_cleaning_report(
            cleaning_result
        )
    )

    # Analysis
    analysis_report = (
        build_analysis_report(
            analysis_result
        )
    )

    # Anomaly
    anomaly_report = (
        build_anomaly_report(
            anomaly_result
        )
    )

    # Machine Learning
    ml_report = (
        build_ml_report(

            ml_recommendations,

            ml_result
        )
    )

    # Final Recommendations
    recommendations = (
        generate_final_recommendations(

            quality_result,

            cleaning_result,

            anomaly_result,

            analysis_result,

            ml_result
        )
    )

    # Build master report
    final_report = (
        build_final_report(

            dataset_report,

            quality_report,

            cleaning_report,

            analysis_report,

            anomaly_report,

            ml_report,

            recommendations
        )
    )

    return final_report