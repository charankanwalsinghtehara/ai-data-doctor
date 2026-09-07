def detect_correlation_insights(
    correlation_result
):

    insights = []

    relationships = (
        correlation_result.get(
            "relationships",
            []
        )
    )

    for relationship in relationships:

        correlation = relationship[
            "correlation"
        ]

        if abs(correlation) >= 0.7:

            insights.append({

                "type":
                    "strong_relationship",

                "priority":
                    "high",

                "message":
                    (
                        f"{relationship['column_1']} "
                        f"and "
                        f"{relationship['column_2']} "
                        f"have a "
                        f"{relationship['strength']} "
                        f"{relationship['direction']} "
                        f"relationship "
                        f"(correlation: "
                        f"{correlation})."
                    )
            })

    return insights


def detect_distribution_insights(
    distribution_results
):

    insights = []

    for column, information in (
        distribution_results.items()
    ):

        if not information.get("available"):
            continue

        shape = (
            information[
                "distribution_shape"
            ]
        )

        if shape != "approximately_symmetric":

            insights.append({

                "type":
                    "distribution",

                "priority":
                    "medium",

                "message":
                    (
                        f"{column} has a "
                        f"{shape} distribution "
                        f"(skewness: "
                        f"{information['skewness']})."
                    )
            })

    return insights


def detect_trend_insights(
    trend_results
):

    insights = []

    for key, information in (
        trend_results.items()
    ):

        trend = information["trend"]

        if trend in [
            "increasing",
            "decreasing"
        ]:

            insights.append({

                "type": "trend",

                "priority": "medium",

                "message":
                    (
                        f"{information['numerical_column']} "
                        f"shows an "
                        f"{trend} trend over "
                        f"{information['date_column']}."
                    )
            })

    return insights


def generate_insights(
    correlation_result,
    distribution_result,
    trend_result
):
    """
    Generate combined insights.
    """

    insights = []

    insights.extend(
        detect_correlation_insights(
            correlation_result
        )
    )

    insights.extend(
        detect_distribution_insights(
            distribution_result
        )
    )

    insights.extend(
        detect_trend_insights(
            trend_result
        )
    )

    return insights