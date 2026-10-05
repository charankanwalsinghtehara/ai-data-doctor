def check_duplicates(dataframe):
    """
    Check duplicate rows.
    """

    total_rows = len(dataframe)

    duplicate_rows = int(
        dataframe.duplicated().sum()
    )

    if total_rows == 0:

        duplicate_percentage = 0

        uniqueness_score = 0

    else:

        duplicate_percentage = round(
            (
                duplicate_rows
                / total_rows
            ) * 100,
            2
        )

        uniqueness_score = round(
            100 - duplicate_percentage,
            2
        )

    return {

        "total_rows":
            total_rows,

        "duplicate_rows":
            duplicate_rows,

        "duplicate_percentage":
            duplicate_percentage,

        "uniqueness_score":
            uniqueness_score
    }