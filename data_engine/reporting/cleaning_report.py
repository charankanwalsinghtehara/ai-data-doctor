def build_cleaning_report(
    cleaning_result
):
    """
    Build cleaning report.
    """

    if not cleaning_result:

        return {

            "available": False,

            "message":
                "Cleaning was not performed."
        }

    return {

        "available": True,

        "summary":
            cleaning_result.get(
                "cleaning_summary",
                {}
            ),

        "recommendations":
            cleaning_result.get(
                "recommendations",
                []
            ),

        "audit_log":
            cleaning_result.get(
                "audit_log",
                []
            )
    }