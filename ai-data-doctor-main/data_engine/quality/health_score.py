def calculate_column_quality_score(
    column_quality_result
):
    """
    Calculate percentage of healthy columns.
    """

    total_columns = len(
        column_quality_result
    )

    if total_columns == 0:

        return 0

    good_columns = 0

    for information in (
        column_quality_result.values()
    ):

        if (
            information["quality_status"]
            == "good"
        ):

            good_columns += 1

    return round(
        (
            good_columns
            / total_columns
        ) * 100,
        2
    )


def calculate_health_score(
    completeness_result,
    duplicate_result,
    column_quality_result
):
    """
    Calculate overall dataset health score.
    """

    completeness = (
        completeness_result[
            "overall_completeness"
        ]
    )

    uniqueness = (
        duplicate_result[
            "uniqueness_score"
        ]
    )

    column_quality = (
        calculate_column_quality_score(
            column_quality_result
        )
    )

    health_score = (

        completeness * 0.50

        + uniqueness * 0.30

        + column_quality * 0.20
    )

    health_score = round(
        health_score,
        2
    )

    if health_score >= 90:

        status = "excellent"

    elif health_score >= 75:

        status = "good"

    elif health_score >= 50:

        status = "needs_attention"

    else:

        status = "poor"

    return {

        "health_score":
            health_score,

        "status":
            status,

        "components": {

            "completeness":
                completeness,

            "uniqueness":
                uniqueness,

            "column_quality":
                column_quality
        }
    }