import os

import numpy as np
import pandas as pd


# =========================================================
# DATASET LOADER
# =========================================================

def load_dataset(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":
        try:
            df = pd.read_csv(file_path)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="latin-1")

    elif extension == ".xlsx":
        df = pd.read_excel(file_path, engine="openpyxl")

    elif extension == ".xls":
        df = pd.read_excel(file_path, engine="xlrd")

    else:
        raise ValueError(
            "Unsupported file format. "
            "Please upload CSV, XLSX, or XLS."
        )

    # Convert column names to strings
    df.columns = df.columns.astype(str)

    return df


# =========================================================
# DATASET OVERVIEW
# =========================================================

def get_dataset_overview(df):
    rows, columns = df.shape

    return {
        "rows": int(rows),
        "columns": int(columns),
        "column_names": df.columns.tolist(),
        "memory_usage_mb": round(
            float(
                df.memory_usage(
                    deep=True
                ).sum()
            ) / (1024 * 1024),
            4
        ),
    }


# =========================================================
# DATA TYPES
# =========================================================

def get_data_types(df):
    return {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }


# =========================================================
# COLUMN TYPES
# =========================================================

def get_column_types(df):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    datetime_columns = df.select_dtypes(
        include=["datetime", "datetimetz"]
    ).columns.tolist()

    return {
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "datetime_columns": datetime_columns,
    }


# =========================================================
# MISSING VALUES
# =========================================================

def analyze_missing_values(df):

    total_rows = len(df)

    missing_count = df.isnull().sum()

    missing_values = {}
    missing_percentage = {}

    for column in df.columns:

        count = int(missing_count[column])

        percentage = (
            round(
                (count / total_rows) * 100,
                2
            )
            if total_rows > 0
            else 0
        )

        missing_values[column] = count
        missing_percentage[column] = percentage

    total_missing = int(
        df.isnull().sum().sum()
    )

    return {
        "total_missing_values": total_missing,
        "missing_values": missing_values,
        "missing_percentage": missing_percentage,
    }


# =========================================================
# DUPLICATES
# =========================================================

def analyze_duplicates(df):

    duplicate_rows = int(
        df.duplicated().sum()
    )

    duplicate_percentage = (
        round(
            duplicate_rows / len(df) * 100,
            2
        )
        if len(df) > 0
        else 0
    )

    return {
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": duplicate_percentage,
    }


# =========================================================
# UNIQUE VALUES
# =========================================================

def analyze_unique_values(df):

    unique_values = {}

    for column in df.columns:

        unique_values[column] = int(
            df[column].nunique(
                dropna=True
            )
        )

    return unique_values


# =========================================================
# NUMERICAL STATISTICS
# =========================================================

def get_numerical_statistics(df):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    results = {}

    for column in numerical_columns:

        series = df[column].dropna()

        if len(series) == 0:

            results[column] = {
                "count": 0,
                "mean": None,
                "median": None,
                "std": None,
                "min": None,
                "max": None,
                "25_percent": None,
                "75_percent": None,
            }

            continue

        results[column] = {
            "count": int(series.count()),
            "mean": round(
                float(series.mean()),
                4
            ),
            "median": round(
                float(series.median()),
                4
            ),
            "std": (
                round(
                    float(series.std()),
                    4
                )
                if len(series) > 1
                else None
            ),
            "min": round(
                float(series.min()),
                4
            ),
            "max": round(
                float(series.max()),
                4
            ),
            "25_percent": round(
                float(series.quantile(0.25)),
                4
            ),
            "75_percent": round(
                float(series.quantile(0.75)),
                4
            ),
        }

    return results


# =========================================================
# CATEGORICAL ANALYSIS
# =========================================================

def get_categorical_statistics(df):

    categorical_columns = df.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    ).columns.tolist()

    results = {}

    for column in categorical_columns:

        series = df[column].dropna()

        if len(series) == 0:

            results[column] = {
                "unique_count": 0,
                "most_frequent": None,
                "most_frequent_count": 0,
            }

            continue

        value_counts = series.value_counts()

        most_frequent = value_counts.index[0]

        most_frequent_count = int(
            value_counts.iloc[0]
        )

        results[column] = {
            "unique_count": int(
                series.nunique()
            ),
            "most_frequent": str(
                most_frequent
            ),
            "most_frequent_count": most_frequent_count,
        }

    return results


# =========================================================
# OUTLIER DETECTION (IQR METHOD)
# =========================================================

def detect_outliers(df):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    results = {}

    for column in numerical_columns:

        series = df[column].dropna()

        if len(series) < 4:

            results[column] = {
                "outlier_count": 0,
                "outlier_percentage": 0,
                "lower_bound": None,
                "upper_bound": None,
            }

            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = series[
            (series < lower_bound)
            |
            (series > upper_bound)
        ]

        outlier_count = int(
            len(outliers)
        )

        outlier_percentage = round(
            (
                outlier_count
                / len(series)
            ) * 100,
            2
        )

        results[column] = {
            "outlier_count": outlier_count,
            "outlier_percentage": outlier_percentage,
            "lower_bound": round(
                float(lower_bound),
                4
            ),
            "upper_bound": round(
                float(upper_bound),
                4
            ),
        }

    return results


# =========================================================
# CORRELATION ANALYSIS
# =========================================================

def analyze_correlations(df):

    numerical_df = df.select_dtypes(
        include=["number"]
    )

    if numerical_df.shape[1] < 2:

        return {
            "correlation_matrix": {},
            "strong_correlations": [],
        }

    correlation_matrix = numerical_df.corr()

    correlation_data = {

        column: {

            other_column: (
                round(
                    float(
                        correlation_matrix.loc[
                            column,
                            other_column
                        ]
                    ),
                    4
                )

                if not pd.isna(
                    correlation_matrix.loc[
                        column,
                        other_column
                    ]
                )

                else None
            )

            for other_column
            in correlation_matrix.columns

        }

        for column
        in correlation_matrix.columns
    }

    strong_correlations = []

    columns = correlation_matrix.columns.tolist()

    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            col1 = columns[i]
            col2 = columns[j]

            correlation = correlation_matrix.loc[
                col1,
                col2
            ]

            if pd.notna(correlation):

                if abs(correlation) >= 0.7:

                    strong_correlations.append({
                        "column_1": col1,
                        "column_2": col2,
                        "correlation": round(
                            float(correlation),
                            4
                        ),
                    })

    return {
        "correlation_matrix": correlation_data,
        "strong_correlations": strong_correlations,
    }


# =========================================================
# DATA QUALITY SCORE
# =========================================================

def calculate_quality_score(
    df,
    missing_analysis,
    duplicate_analysis,
    outlier_analysis
):

    if len(df) == 0:

        return {
            "score": 0,
            "grade": "F",
            "message": "Dataset is empty."
        }

    total_cells = df.shape[0] * df.shape[1]

    missing_count = (
        missing_analysis[
            "total_missing_values"
        ]
    )

    missing_percentage = (
        missing_count / total_cells * 100
        if total_cells > 0
        else 0
    )

    duplicate_percentage = (
        duplicate_analysis[
            "duplicate_percentage"
        ]
    )

    total_outliers = sum(
        item["outlier_count"]
        for item in outlier_analysis.values()
    )

    numerical_cells = (
        len(df)
        *
        len(
            df.select_dtypes(
                include=["number"]
            ).columns
        )
    )

    outlier_percentage = (
        total_outliers
        / numerical_cells
        * 100
        if numerical_cells > 0
        else 0
    )

    score = 100

    # Missing values penalty
    score -= min(
        missing_percentage * 0.5,
        40
    )

    # Duplicate penalty
    score -= min(
        duplicate_percentage * 0.5,
        25
    )

    # Outlier penalty
    score -= min(
        outlier_percentage * 0.2,
        20
    )

    score = max(
        0,
        round(score, 2)
    )

    if score >= 90:

        grade = "A"
        message = "Excellent data quality."

    elif score >= 75:

        grade = "B"
        message = "Good data quality."

    elif score >= 60:

        grade = "C"
        message = "Average data quality."

    elif score >= 40:

        grade = "D"
        message = "Poor data quality."

    else:

        grade = "F"
        message = "Very poor data quality."

    return {
        "score": score,
        "grade": grade,
        "message": message,
    }


# =========================================================
# CLEANING RECOMMENDATIONS
# =========================================================

def generate_cleaning_recommendations(
    df,
    missing_analysis,
    duplicate_analysis,
    outlier_analysis
):

    recommendations = []

    # Missing values recommendations
    for column in df.columns:

        missing_count = (
            missing_analysis[
                "missing_values"
            ][column]
        )

        missing_percentage = (
            missing_analysis[
                "missing_percentage"
            ][column]
        )

        if missing_count > 0:

            if missing_percentage > 50:

                suggestion = (
                    "More than 50% values are missing. "
                    "Consider removing this column."
                )

            elif pd.api.types.is_numeric_dtype(
                df[column]
            ):

                suggestion = (
                    "Consider filling missing values "
                    "with median or mean."
                )

            else:

                suggestion = (
                    "Consider filling missing values "
                    "with mode or 'Unknown'."
                )

            recommendations.append({

                "issue": "Missing Values",

                "column": column,

                "severity": (
                    "high"
                    if missing_percentage > 30
                    else "medium"
                ),

                "recommendation": suggestion,

            })

    # Duplicate recommendation
    if (
        duplicate_analysis[
            "duplicate_rows"
        ] > 0
    ):

        recommendations.append({

            "issue": "Duplicate Rows",

            "column": None,

            "severity": "medium",

            "recommendation": (
                "Remove duplicate rows to "
                "improve dataset quality."
            ),

        })

    # Outlier recommendations
    for column, result in outlier_analysis.items():

        if result["outlier_count"] > 0:

            recommendations.append({

                "issue": "Outliers",

                "column": column,

                "severity": (
                    "high"
                    if result[
                        "outlier_percentage"
                    ] > 10
                    else "medium"
                ),

                "recommendation": (
                    "Review outliers using IQR bounds. "
                    "Consider removing, capping, or "
                    "transforming extreme values."
                ),

            })

    # Constant columns
    for column in df.columns:

        unique_count = df[column].nunique(
            dropna=True
        )

        if unique_count <= 1:

            recommendations.append({

                "issue": "Constant Column",

                "column": column,

                "severity": "low",

                "recommendation": (
                    "This column contains only one unique "
                    "value and may not be useful for analysis."
                ),

            })

    return recommendations


# =========================================================
# DATASET INSIGHTS
# =========================================================

def generate_insights(
    df,
    missing_analysis,
    duplicate_analysis,
    outlier_analysis,
    correlation_analysis
):

    insights = []

    # Dataset size
    insights.append(
        f"The dataset contains {len(df)} rows "
        f"and {len(df.columns)} columns."
    )

    # Missing values
    total_missing = (
        missing_analysis[
            "total_missing_values"
        ]
    )

    if total_missing > 0:

        insights.append(
            f"The dataset contains "
            f"{total_missing} missing values."
        )

    else:

        insights.append(
            "No missing values were detected."
        )

    # Duplicates
    duplicate_rows = (
        duplicate_analysis[
            "duplicate_rows"
        ]
    )

    if duplicate_rows > 0:

        insights.append(
            f"{duplicate_rows} duplicate rows "
            f"were detected."
        )

    else:

        insights.append(
            "No duplicate rows were detected."
        )

    # Outliers
    columns_with_outliers = [

        column

        for column, result
        in outlier_analysis.items()

        if result["outlier_count"] > 0

    ]

    if columns_with_outliers:

        insights.append(
            "Outliers were detected in: "
            + ", ".join(
                columns_with_outliers
            )
        )

    else:

        insights.append(
            "No significant outliers were detected."
        )

    # Correlation
    strong_correlations = (
        correlation_analysis[
            "strong_correlations"
        ]
    )

    if strong_correlations:

        insights.append(
            f"{len(strong_correlations)} strong "
            f"correlation relationship(s) were detected."
        )

    else:

        insights.append(
            "No strong correlations were detected."
        )

    return insights


# =========================================================
# COMPLETE DATASET ANALYSIS
# =========================================================

def analyze_dataset(file_path):

    # Load dataset
    df = load_dataset(file_path)

    # Basic analysis
    overview = get_dataset_overview(df)

    data_types = get_data_types(df)

    column_types = get_column_types(df)

    missing_analysis = analyze_missing_values(df)

    duplicate_analysis = analyze_duplicates(df)

    unique_values = analyze_unique_values(df)

    # Statistics
    numerical_statistics = get_numerical_statistics(df)

    categorical_statistics = get_categorical_statistics(df)

    # Advanced analysis
    outlier_analysis = detect_outliers(df)

    correlation_analysis = analyze_correlations(df)

    # Data quality
    quality_score = calculate_quality_score(

        df,

        missing_analysis,

        duplicate_analysis,

        outlier_analysis,

    )

    # Recommendations
    cleaning_recommendations = (
        generate_cleaning_recommendations(

            df,

            missing_analysis,

            duplicate_analysis,

            outlier_analysis,

        )
    )

    # Insights
    insights = generate_insights(

        df,

        missing_analysis,

        duplicate_analysis,

        outlier_analysis,

        correlation_analysis,

    )

    # Final result
    return {

        "dataset_overview": overview,

        "data_types": data_types,

        "column_types": column_types,

        "missing_values": missing_analysis,

        "duplicates": duplicate_analysis,

        "unique_values": unique_values,

        "numerical_statistics": numerical_statistics,

        "categorical_statistics": categorical_statistics,

        "outliers": outlier_analysis,

        "correlation_analysis": correlation_analysis,

        "data_quality": quality_score,

        "cleaning_recommendations": cleaning_recommendations,

        "insights": insights,

    }


# =========================================================
# AUTOMATIC DATA CLEANING
# =========================================================

def clean_dataset(file_path):

    df = load_dataset(file_path)

    original_rows = len(df)

    original_columns = len(df.columns)

    cleaning_actions = []

    # Remove duplicate rows
    duplicates_before = int(
        df.duplicated().sum()
    )

    if duplicates_before > 0:

        df = df.drop_duplicates()

        cleaning_actions.append({

            "action": "Removed duplicate rows",

            "rows_removed": duplicates_before,

        })

    # Handle missing values
    for column in df.columns.tolist():

        missing_count = int(
            df[column].isnull().sum()
        )

        if missing_count == 0:

            continue

        missing_percentage = (
            missing_count / len(df) * 100
            if len(df) > 0
            else 0
        )

        # Remove column if more than 50% missing
        if missing_percentage > 50:

            df = df.drop(
                columns=[column]
            )

            cleaning_actions.append({

                "action": "Removed column",

                "column": column,

                "reason": (
                    "More than 50% missing values"
                ),

            })

        # Numerical -> Median
        elif pd.api.types.is_numeric_dtype(
            df[column]
        ):

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )

            cleaning_actions.append({

                "action": "Filled missing values",

                "column": column,

                "method": "median",

            })

        # Categorical -> Mode
        else:

            mode_values = df[column].mode()

            if len(mode_values) > 0:

                fill_value = mode_values.iloc[0]

            else:

                fill_value = "Unknown"

            df[column] = df[column].fillna(
                fill_value
            )

            cleaning_actions.append({

                "action": "Filled missing values",

                "column": column,

                "method": "mode",

            })

    return {

        "dataframe": df,

        "summary": {

            "original_rows": original_rows,

            "original_columns": original_columns,

            "cleaned_rows": len(df),

            "cleaned_columns": len(df.columns),

            "actions": cleaning_actions,

        },

    }