import pandas as pd


def classify_dataset(dataframe):
    """
    Identify the general type
    of dataset.
    """

    if not isinstance(dataframe, pd.DataFrame):

        raise TypeError(
            "Expected a Pandas DataFrame."
        )


    rows, columns = dataframe.shape


    numeric_columns = len(

        dataframe.select_dtypes(
            include=["number"]
        ).columns
    )


    categorical_columns = len(

        dataframe.select_dtypes(
            include=["object", "category"]
        ).columns
    )


    datetime_columns = len(

        dataframe.select_dtypes(
            include=["datetime"]
        ).columns
    )


    total_columns = max(columns, 1)


    numeric_ratio = (
        numeric_columns / total_columns
    )


    categorical_ratio = (
        categorical_columns / total_columns
    )


    if datetime_columns > 0:

        dataset_type = "time_related"


    elif numeric_ratio >= 0.7:

        dataset_type = "numerical"


    elif categorical_ratio >= 0.7:

        dataset_type = "categorical"


    else:

        dataset_type = "mixed"


    return {

        "dataset_type":
            dataset_type,

        "rows":
            rows,

        "columns":
            columns,

        "numeric_columns":
            numeric_columns,

        "categorical_columns":
            categorical_columns,

        "datetime_columns":
            datetime_columns
    }