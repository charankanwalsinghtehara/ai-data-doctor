import pandas as pd

from .exceptions import (
    UnsupportedCleaningDataError
)

from .missing_handler import (
    handle_missing_values
)

from .duplicate_cleaner import (
    remove_duplicate_rows
)

from .category_normalizer import (
    normalize_categories
)

from .datatype_converter import (
    convert_detected_datatypes
)

from .outlier_handler import (
    handle_outliers
)

from .strategy_engine import (
    generate_cleaning_strategy
)

from .audit_logger import (
    create_audit_log,
    add_audit_entry
)

from .column_cleaner import (
    remove_empty_columns
)

def clean_dataset(
    dataframe,
    understanding_result,
    quality_result,
    auto_clean=True
):
    """
    Complete Data Cleaning Pipeline.

    Original dataframe is never modified.
    """

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise UnsupportedCleaningDataError(
            "Cleaning Engine supports "
            "Pandas DataFrames only."
        )

    # Keep original data untouched
    original_dataframe = dataframe.copy()

    # Working copy
    cleaned_dataframe = dataframe.copy()

    # Create audit history
    audit_log = create_audit_log()

    # Generate recommendations
    recommendations = (
        generate_cleaning_strategy(
            dataframe,
            understanding_result,
            quality_result
        )
    )

    # If automatic cleaning is disabled
    if not auto_clean:

        return {

            "success": True,

            "original_data":
                original_dataframe,

            "cleaned_data":
                cleaned_dataframe,

            "recommendations":
                recommendations,

            "audit_log":
                audit_log
        }

    # STEP 1: Remove duplicates
    cleaned_dataframe, duplicate_result = (
        remove_duplicate_rows(
            cleaned_dataframe
        )
    )

    add_audit_entry(
        audit_log,
        "remove_duplicates",
        duplicate_result
    )


    # STEP:3 Remove completely empty columns
    cleaned_dataframe, empty_column_result = (
        remove_empty_columns(
            cleaned_dataframe
        )
    )

    add_audit_entry(
    audit_log,
    "remove_empty_columns",
    empty_column_result
)

    # STEP 2: Handle missing values
    cleaned_dataframe, missing_result = (
        handle_missing_values(
            cleaned_dataframe,
            understanding_result
        )
    )

    add_audit_entry(
        audit_log,
        "handle_missing_values",
        missing_result
    )

    # STEP 3: Normalize categories
    cleaned_dataframe, category_result = (
        normalize_categories(
            cleaned_dataframe,
            understanding_result
        )
    )

    add_audit_entry(
        audit_log,
        "normalize_categories",
        category_result
    )

    # STEP 4: Convert datatypes
    cleaned_dataframe, datatype_result = (
        convert_detected_datatypes(
            cleaned_dataframe,
            understanding_result
        )
    )

    add_audit_entry(
        audit_log,
        "convert_datatypes",
        datatype_result
    )

    # STEP 5: Handle outliers
    cleaned_dataframe, outlier_result = (
        handle_outliers(
            cleaned_dataframe
        )
    )

    add_audit_entry(
        audit_log,
        "handle_outliers",
        outlier_result
    )

    return {

        "success": True,

        "original_data":
            original_dataframe,

        "cleaned_data":
            cleaned_dataframe,

        "recommendations":
            recommendations,

        "audit_log":
            audit_log,

        "cleaning_summary": {

            "original_rows":
                len(original_dataframe),

            "cleaned_rows":
                len(cleaned_dataframe),

            "original_columns":
                len(original_dataframe.columns),

            "cleaned_columns":
                len(cleaned_dataframe.columns)
        }
    }