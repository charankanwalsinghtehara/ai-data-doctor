import pandas as pd

from .exceptions import (
    UnsupportedAnalysisDataError
)

from .correlation_analysis import (
    analyze_correlations
)

from .distribution_analysis import (
    analyze_all_distributions
)

from .relationship_analysis import (
    analyze_categorical_numerical
)

from .trend_analysis import (
    analyze_time_trends
)

from .statistical_tests import (
    analyze_basic_statistics
)

from .insight_detector import (
    generate_insights
)


def analyze_dataset(
    dataframe,
    understanding_result
):
    """
    Complete Data Analysis Pipeline.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedAnalysisDataError(
            "Analysis Engine supports "
            "Pandas DataFrames only."
        )

    # Correlation analysis
    correlation_result = (
        analyze_correlations(
            dataframe
        )
    )

    # Distribution analysis
    distribution_result = (
        analyze_all_distributions(
            dataframe
        )
    )

    # Categorical vs numerical
    relationship_result = (
        analyze_categorical_numerical(
            dataframe,
            understanding_result
        )
    )

    # Time trends
    trend_result = (
        analyze_time_trends(
            dataframe,
            understanding_result
        )
    )

    # Statistical observations
    statistical_result = (
        analyze_basic_statistics(
            distribution_result
        )
    )

    # Human-readable insights
    insights = (
        generate_insights(
            correlation_result,
            distribution_result,
            trend_result
        )
    )

    return {

        "success": True,

        "correlations":
            correlation_result,

        "distributions":
            distribution_result,

        "relationships":
            relationship_result,

        "trends":
            trend_result,

        "statistics":
            statistical_result,

        "insights":
            insights
    }