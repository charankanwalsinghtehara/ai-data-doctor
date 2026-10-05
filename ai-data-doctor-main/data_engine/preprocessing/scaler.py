from sklearn.preprocessing import (
    StandardScaler
)


def scale_numeric_features(
    dataframe
):
    """
    Scale numeric features.
    """

    dataframe = dataframe.copy()


    numeric_columns = (

        dataframe.select_dtypes(
            include=["number"]
        ).columns
    )


    if len(
        numeric_columns
    ) == 0:

        return dataframe


    scaler = StandardScaler()


    dataframe[
        numeric_columns
    ] = scaler.fit_transform(

        dataframe[
            numeric_columns
        ]
    )


    return dataframe