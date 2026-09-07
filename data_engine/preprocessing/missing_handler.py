import pandas as pd


def handle_missing_values(
    dataframe
):
    """
    Handle missing values
    for machine learning.
    """

    dataframe = dataframe.copy()


    numeric_columns = (

        dataframe.select_dtypes(
            include=["number"]
        ).columns
    )


    categorical_columns = (

        dataframe.select_dtypes(
            exclude=["number"]
        ).columns
    )


    # =========================
    # NUMERIC COLUMNS
    # =========================

    for column in numeric_columns:

        if dataframe[column].isnull().any():

            median_value = (

                dataframe[column]
                .median()
            )

            dataframe[column] = (

                dataframe[column]
                .fillna(
                    median_value
                )
            )


    # =========================
    # CATEGORICAL COLUMNS
    # =========================

    for column in categorical_columns:

        if dataframe[column].isnull().any():

            dataframe[column] = (

                dataframe[column]
                .fillna(
                    "Unknown"
                )
            )


    return dataframe