def build_quality_report(
    quality_result
):
    """
    Build data quality report.
    """

    if not quality_result:

        return {

            "available": False,

            "message":
                "Quality analysis not available."
        }

    report = {

        "available": True,

        "completeness":
            quality_result.get(
                "completeness",
                {}
            ),

        "duplicates":
            quality_result.get(
                "duplicates",
                {}
            ),

        "column_quality":
            quality_result.get(
                "column_quality",
                {}
            )
    }

    # Add health score if available
    if "health_score" in quality_result:

        report["health_score"] = (
            quality_result[
                "health_score"
            ]
        )

    return report