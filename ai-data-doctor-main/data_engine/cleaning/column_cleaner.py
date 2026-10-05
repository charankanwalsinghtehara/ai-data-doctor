def remove_empty_columns(dataframe):
    """
    Remove columns where every value is missing.
    """

    empty_columns = []

    for column in dataframe.columns:

        if dataframe[column].isna().all():

            empty_columns.append(column)

    cleaned_dataframe = dataframe.drop(
        columns=empty_columns
    )

    return cleaned_dataframe, {

        "removed_columns":
            empty_columns,

        "total_removed":
            len(empty_columns)
    }