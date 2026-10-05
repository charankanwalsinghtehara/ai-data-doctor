def profile_duplicates(dataframe):
    """
    Analyze duplicate rows.
    """

    total_rows = len(dataframe)

    duplicate_count = int(
        dataframe.duplicated().sum()
    )

    if total_rows > 0:

        duplicate_percentage = round(
            (duplicate_count / total_rows) * 100,
            2
        )

    else:

        duplicate_percentage = 0

    return {
        "duplicate_rows":
            duplicate_count,

        "duplicate_percentage":
            duplicate_percentage,

        "unique_rows":
            int(total_rows - duplicate_count)
    }