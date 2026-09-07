def build_analysis_report(
    analysis_result
):
    """
    Build data analysis report.
    """

    if not analysis_result:

        return {

            "available": False,

            "message":
                "Analysis not available."
        }

    return {

        "available": True,

        "correlations":
            analysis_result.get(
                "correlations",
                {}
            ),

        "distributions":
            analysis_result.get(
                "distributions",
                {}
            ),

        "relationships":
            analysis_result.get(
                "relationships",
                {}
            ),

        "trends":
            analysis_result.get(
                "trends",
                {}
            ),

        "statistics":
            analysis_result.get(
                "statistics",
                {}
            ),

        "insights":
            analysis_result.get(
                "insights",
                []
            )
    }