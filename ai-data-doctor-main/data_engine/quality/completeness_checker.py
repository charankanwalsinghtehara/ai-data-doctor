def check_completeness(dataframe):
    """
    Calculate dataset completeness.
    """

    total_cells = (
        dataframe.shape[0]
        * dataframe.shape[1]
    )

    total_missing = int(
        dataframe.isna().sum().sum()
    )

    if total_cells == 0:

        completeness_score = 0

    else:

        completeness_score = round(
            (
                (total_cells - total_missing)
                / total_cells
            ) * 100,
            2
        )

    column_results = {}

    for column in dataframe.columns:

        total_rows = len(dataframe)

        missing_count = int(
            dataframe[column]
            .isna()
            .sum()
        )

        if total_rows == 0:

            completeness = 0

        else:

            completeness = round(
                (
                    (total_rows - missing_count)
                    / total_rows
                ) * 100,
                2
            )

        column_results[column] = {

            "missing_values":
                missing_count,

            "completeness_percentage":
                completeness
        }

    return {

        "overall_completeness":
            completeness_score,

        "total_missing_values":
            total_missing,

        "columns":
            column_results
    }