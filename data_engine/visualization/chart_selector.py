def select_visualizations(
    dataframe
):
    """
    Decide which visualization types
    should be generated.
    """

    decisions = {

        "missing_values": False,

        "distributions": False,

        "categorical": False,

        "correlation": False,

        "outliers": False,

        "trends": False
    }

    # Missing values

    if dataframe.isnull().sum().sum() > 0:

        decisions[
            "missing_values"
        ] = True

    # Numeric columns

    numeric_columns = (

        dataframe.select_dtypes(
            include="number"
        )

        .columns
    )

    if len(numeric_columns) > 0:

        decisions[
            "distributions"
        ] = True

        decisions[
            "outliers"
        ] = True

    if len(numeric_columns) >= 2:

        decisions[
            "correlation"
        ] = True

    # Categorical columns

    categorical_columns = (

        dataframe.select_dtypes(

            include=[
                "object",
                "category"
            ]
        )

        .columns
    )

    if len(categorical_columns) > 0:

        decisions[
            "categorical"
        ] = True

    # Datetime columns

    datetime_columns = (

        dataframe.select_dtypes(

            include=[
                "datetime",
                "datetimetz"
            ]
        )

        .columns
    )

    if (

        len(datetime_columns) > 0

        and

        len(numeric_columns) > 0

    ):

        decisions[
            "trends"
        ] = True

    return decisions