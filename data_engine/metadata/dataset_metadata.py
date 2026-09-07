import pandas as pd


def get_dataset_metadata(
    dataframe
):
    """
    Collect metadata about
    the extracted dataset.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise TypeError(
            "Expected a Pandas DataFrame."
        )


    column_names = [

        str(column)

        for column in dataframe.columns
    ]


    column_data_types = {

        str(column):

        str(
            dataframe[column].dtype
        )

        for column in dataframe.columns
    }


    memory_usage_bytes = (

        dataframe.memory_usage(
            deep=True
        ).sum()
    )


    memory_usage_mb = (

        memory_usage_bytes
        / (1024 * 1024)
    )


    return {

        "rows":

            int(
                dataframe.shape[0]
            ),

        "columns":

            int(
                dataframe.shape[1]
            ),

        "column_names":

            column_names,

        "column_data_types":

            column_data_types,

        "memory_usage_bytes":

            int(
                memory_usage_bytes
            ),

        "memory_usage_mb":

            round(
                memory_usage_mb,
                4
            ),

        "empty_dataset":

            dataframe.empty
    }