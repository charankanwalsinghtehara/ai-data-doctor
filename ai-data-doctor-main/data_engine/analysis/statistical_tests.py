def analyze_basic_statistics(
    distribution_results
):
    """
    Generate statistical observations
    from distribution analysis.
    """

    results = {}

    for column, information in (
        distribution_results.items()
    ):

        if not information.get("available"):

            continue

        skewness = information[
            "skewness"
        ]

        shape = information[
            "distribution_shape"
        ]

        results[column] = {

            "skewness":
                skewness,

            "distribution_shape":
                shape,

            "mean":
                information["mean"],

            "median":
                information["median"]
        }

    return results