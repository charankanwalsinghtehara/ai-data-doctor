import pandas as pd


def encode_categorical_columns(
    dataframe
):
    """
    Convert categorical columns
    into numerical features.
    """

    dataframe = dataframe.copy()


    categorical_columns = (

        dataframe.select_dtypes(
            include=["object", "category"]
        ).columns
    )


    if len(
        categorical_columns
    ) == 0:

        return dataframe


    encoded_dataframe = (

        pd.get_dummies(

            dataframe,

            columns=categorical_columns,

            drop_first=True,

            dtype=int
        )
    )


    return encoded_dataframe