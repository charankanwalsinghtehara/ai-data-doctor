import pandas as pd


def build_dataset_report(
    dataframe,
    understanding_result=None,
    profiling_result=None
):
    """
    Build the dataset overview section.
    """

    report = {

        "rows": int(len(dataframe)),

        "columns": int(len(dataframe.columns)),

        "column_names":
            dataframe.columns.tolist(),

        "memory_usage_bytes":
            int(
                dataframe
                .memory_usage(
                    deep=True
                )
                .sum()
            ),

        "data_types": {

            column:
            str(dataframe[column].dtype)

            for column
            in dataframe.columns
        }
    }

    if understanding_result:

        report["understanding"] = (
            understanding_result
        )

    if profiling_result:

        report["profiling"] = (
            profiling_result
        )

    return report