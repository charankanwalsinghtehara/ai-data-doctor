def remove_duplicate_rows(dataframe):
    """
    Remove completely duplicate rows.
    """

    rows_before = len(dataframe)

    cleaned_dataframe = (
        dataframe
        .drop_duplicates()
        .copy()
    )

    rows_after = len(cleaned_dataframe)

    removed_rows = (
        rows_before - rows_after
    )

    return cleaned_dataframe, {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "duplicates_removed": removed_rows
    }