def check_column_quality(dataframe):
    """
    Detect column-level quality problems.
    """

    results = {}

    total_rows = len(dataframe)

    for column in dataframe.columns:

        series = dataframe[column]

        non_null = series.dropna()

        unique_count = int(
            series.nunique()
        )

        missing_count = int(
            series.isna().sum()
        )

        issues = []

        # Completely empty column
        if non_null.empty:

            issues.append(
                "completely_empty"
            )

        # Only one unique value
        if (
            not non_null.empty
            and unique_count == 1
        ):

            issues.append(
                "constant_value"
            )

        # Very high missing percentage
        if total_rows > 0:

            missing_percentage = round(
                (
                    missing_count
                    / total_rows
                ) * 100,
                2
            )

        else:

            missing_percentage = 0

        if missing_percentage >= 50:

            issues.append(
                "high_missing_values"
            )

        # High cardinality
        if (
            total_rows > 0
            and unique_count / total_rows
            > 0.95
        ):

            issues.append(
                "high_cardinality"
            )

        results[column] = {

            "unique_values":
                unique_count,

            "missing_values":
                missing_count,

            "missing_percentage":
                missing_percentage,

            "issues":
                issues,

            "quality_status":
                (
                    "problem"
                    if issues
                    else "good"
                )
        }

    return results