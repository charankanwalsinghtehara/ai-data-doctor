def generate_cleaning_strategy(
    dataframe,
    understanding_result,
    quality_result
):
    """
    Generate recommended cleaning actions.
    """

    recommendations = []

    # Missing values
    completeness = (
        quality_result["completeness"]
    )

    total_missing = (
        completeness[
            "total_missing_values"
        ]
    )

    if total_missing > 0:

        recommendations.append({
            "priority": "high",
            "issue": "missing_values",
            "action":
                "Apply role-based missing "
                "value handling"
        })

    # Duplicate rows
    duplicates = (
        quality_result["duplicates"]
    )

    duplicate_rows = (
        duplicates["duplicate_rows"]
    )

    if duplicate_rows > 0:

        recommendations.append({
            "priority": "high",
            "issue": "duplicate_rows",
            "action":
                "Remove completely duplicate rows"
        })

    # Column issues
    column_quality = (
        quality_result["column_quality"]
    )

    for column, information in (
        column_quality.items()
    ):

        issues = information["issues"]

        for issue in issues:

            if issue == "constant_value":

                recommendations.append({

                    "priority": "medium",

                    "column": column,

                    "issue":
                        "constant_value",

                    "action":
                        "Consider removing "
                        "the column"
                })

            elif issue == "completely_empty":

                recommendations.append({

                    "priority": "high",

                    "column": column,

                    "issue":
                        "completely_empty",

                    "action":
                        "Remove empty column"
                })

    # Categorical normalization
    for column, information in (
        understanding_result["columns"]
        .items()
    ):

        if (
            information.get("role")
            == "categorical"
        ):

            recommendations.append({

                "priority": "low",

                "column": column,

                "issue":
                    "category_formatting",

                "action":
                    "Normalize category values"
            })

    return recommendations