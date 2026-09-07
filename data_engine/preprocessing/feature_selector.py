def prepare_features_and_target(

    dataframe,

    target_column
):
    """
    Separate features and target.
    """

    if target_column not in dataframe.columns:

        raise ValueError(

            f"Target column not found: "
            f"{target_column}"
        )


    X = dataframe.drop(

        columns=[
            target_column
        ]
    )


    y = dataframe[
        target_column
    ]


    return X, y