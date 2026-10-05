import pandas as pd

from .exceptions import (
    VisualizationError
)

from .paths import (
    get_visualization_directory
)

from .chart_selector import (
    select_visualizations
)

from .missing_values import (
    create_missing_values_chart
)

from .distributions import (
    create_distribution_charts
)

from .categorical import (
    create_categorical_charts
)

from .correlation import (
    create_correlation_chart
)

from .outliers import (
    create_outlier_charts
)

from .trends import (
    create_trend_charts
)


def run_visualization_engine(
    dataframe,
    project_id
):
    """
    Run complete automatic
    visualization pipeline.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise VisualizationError(

            "Visualization Engine supports "
            "Pandas DataFrames only."
        )

    output_directory = (
        get_visualization_directory(
            project_id
        )
    )

    decisions = (
        select_visualizations(
            dataframe
        )
    )

    results = {

        "project_id":
            project_id,

        "visualizations": {}
    }

    # -------------------------
    # MISSING VALUES
    # -------------------------

    if decisions["missing_values"]:

        chart = (
            create_missing_values_chart(

                dataframe,

                output_directory
            )
        )

        results["visualizations"][
            "missing_values"
        ] = chart

    # -------------------------
    # DISTRIBUTIONS
    # -------------------------

    if decisions["distributions"]:

        charts = (
            create_distribution_charts(

                dataframe,

                output_directory
            )
        )

        results["visualizations"][
            "distributions"
        ] = charts

    # -------------------------
    # CATEGORICAL
    # -------------------------

    if decisions["categorical"]:

        charts = (
            create_categorical_charts(

                dataframe,

                output_directory
            )
        )

        results["visualizations"][
            "categorical"
        ] = charts

    # -------------------------
    # CORRELATION
    # -------------------------

    if decisions["correlation"]:

        chart = (
            create_correlation_chart(

                dataframe,

                output_directory
            )
        )

        results["visualizations"][
            "correlation"
        ] = chart

    # -------------------------
    # OUTLIERS
    # -------------------------

    if decisions["outliers"]:

        charts = (
            create_outlier_charts(

                dataframe,

                output_directory
            )
        )

        results["visualizations"][
            "outliers"
        ] = charts

    # -------------------------
    # TRENDS
    # -------------------------

    if decisions["trends"]:

        charts = (
            create_trend_charts(

                dataframe,

                output_directory
            )
        )

        results["visualizations"][
            "trends"
        ] = charts

    results["total_chart_groups"] = (
        len(
            results[
                "visualizations"
            ]
        )
    )

    return results