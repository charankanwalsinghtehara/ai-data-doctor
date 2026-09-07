import pandas as pd

from .exceptions import (
    UnsupportedQualityDataError
)

from .completeness_checker import (
    check_completeness
)

from .duplicate_checker import (
    check_duplicates
)

from .column_quality_checker import (
    check_column_quality
)

from .consistency_checker import (
    check_consistency
)

from .health_score import (
    calculate_health_score
)


def check_data_quality(
    dataframe,
    understanding_result
):
    """
    Complete Data Quality pipeline.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedQualityDataError(
            "Quality Engine supports "
            "Pandas DataFrames only."
        )

    completeness_result = (
        check_completeness(dataframe)
    )

    duplicate_result = (
        check_duplicates(dataframe)
    )

    column_quality_result = (
        check_column_quality(dataframe)
    )

    consistency_result = (
        check_consistency(
            dataframe,
            understanding_result
        )
    )

    health_result = (
        calculate_health_score(
            completeness_result,
            duplicate_result,
            column_quality_result
        )
    )

    return {

        "success": True,

        "completeness":
            completeness_result,

        "duplicates":
            duplicate_result,

        "column_quality":
            column_quality_result,

        "consistency":
            consistency_result,

        "health":
            health_result
    }