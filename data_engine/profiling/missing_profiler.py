def profile_missing_values(dataframe):
    """
    Analyze missing values in every column.
    """

    total_rows = len(dataframe)

    results = {}

    total_missing = 0

    for column in dataframe.columns:

        missing_count = int(
            dataframe[column]
            .isna()
            .sum()
        )

        total_missing += missing_count

        if total_rows > 0:

            missing_percentage = round(
                (missing_count / total_rows) * 100,
                2
            )

        else:

            missing_percentage = 0

        results[column] = {
            "missing_count": missing_count,
            "missing_percentage":
                missing_percentage
        }

    return {
        "total_missing_values":
            total_missing,

        "columns":
            results
    }