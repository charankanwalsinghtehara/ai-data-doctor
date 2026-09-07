import pandas as pd
import numpy as np


def convert_to_python(value):
    """
    Convert NumPy/Pandas values into normal Python values
    so they can be returned in JSON responses.
    """

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        if np.isnan(value):
            return None
        return float(value)

    if isinstance(value, (np.bool_,)):
        return bool(value)

    return value


def detect_missing_values(df):
    """
    Detect missing values and generate recommendations.
    """

    issues = []

    total_rows = len(df)

    for column in df.columns:

        missing_count = int(df[column].isnull().sum())

        if missing_count > 0:

            missing_percentage = (
                missing_count / total_rows * 100
                if total_rows > 0
                else 0
            )

            recommendation = "Investigate missing values."

            if missing_percentage < 5:
                recommendation = (
                    "Small amount of missing data. "
                    "Consider removing affected rows or imputing values."
                )

            elif missing_percentage < 30:
                recommendation = (
                    "Moderate missing data. "
                    "Consider median/mean imputation for numerical columns "
                    "or mode imputation for categorical columns."
                )

            else:
                recommendation = (
                    "Large amount of missing data. "
                    "Consider dropping this column if it is not important."
                )

            issues.append({
                "column": column,
                "missing_count": missing_count,
                "missing_percentage": round(
                    float(missing_percentage),
                    2
                ),
                "recommendation": recommendation,
            })

    return issues


def detect_duplicates(df):
    """
    Detect duplicate rows.
    """

    duplicate_count = int(df.duplicated().sum())

    recommendation = "No duplicate rows found."

    if duplicate_count > 0:
        recommendation = (
            "Remove duplicate rows to prevent biased analysis "
            "and incorrect machine learning results."
        )

    return {
        "duplicate_rows": duplicate_count,
        "recommendation": recommendation,
    }


def detect_constant_columns(df):
    """
    Detect columns containing only one unique value.
    """

    constant_columns = []

    for column in df.columns:

        unique_count = df[column].nunique(dropna=False)

        if unique_count <= 1:

            constant_columns.append({
                "column": column,
                "unique_values": int(unique_count),
                "recommendation": (
                    "Consider removing this column because it "
                    "contains no useful variation."
                ),
            })

    return constant_columns


def detect_high_cardinality_columns(df):
    """
    Detect categorical columns with many unique values.
    """

    issues = []

    total_rows = len(df)

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        unique_count = int(df[column].nunique())

        unique_percentage = (
            unique_count / total_rows * 100
            if total_rows > 0
            else 0
        )

        if unique_percentage > 50:

            issues.append({
                "column": column,
                "unique_values": unique_count,
                "unique_percentage": round(
                    float(unique_percentage),
                    2
                ),
                "recommendation": (
                    "High-cardinality categorical column detected. "
                    "Check whether this is an ID column or consider "
                    "encoding techniques suitable for high-cardinality data."
                ),
            })

    return issues


def detect_outliers(df):
    """
    Detect outliers using the IQR method.
    """

    outlier_results = []

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for column in numerical_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = series[
            (series < lower_bound)
            | (series > upper_bound)
        ]

        outlier_count = len(outliers)

        if outlier_count > 0:

            outlier_percentage = (
                outlier_count / len(series) * 100
            )

            outlier_results.append({
                "column": column,
                "outlier_count": int(outlier_count),
                "outlier_percentage": round(
                    float(outlier_percentage),
                    2
                ),
                "lower_bound": round(
                    float(lower_bound),
                    4
                ),
                "upper_bound": round(
                    float(upper_bound),
                    4
                ),
                "recommendation": (
                    "Investigate outliers. Consider capping, "
                    "transforming, or removing extreme values "
                    "depending on the business context."
                ),
            })

    return outlier_results


def detect_data_types(df):
    """
    Analyze column data types.
    """

    results = []

    for column in df.columns:

        dtype = str(df[column].dtype)

        results.append({
            "column": column,
            "data_type": dtype,
        })

    return results


def calculate_data_quality_score(
    df,
    missing_issues,
    duplicate_info,
    constant_columns
):
    """
    Calculate a simple Data Quality Score out of 100.
    """

    score = 100

    total_cells = df.shape[0] * df.shape[1]

    total_missing = int(df.isnull().sum().sum())

    if total_cells > 0:

        missing_percentage = (
            total_missing / total_cells * 100
        )

        score -= missing_percentage * 0.5

    duplicate_rows = duplicate_info["duplicate_rows"]

    if len(df) > 0:

        duplicate_percentage = (
            duplicate_rows / len(df) * 100
        )

        score -= duplicate_percentage * 0.5

    score -= len(constant_columns) * 5

    score = max(0, min(100, score))

    return round(float(score), 2)


def calculate_ml_readiness_score(
    df,
    missing_issues,
    duplicate_info,
    constant_columns,
    outliers
):
    """
    Calculate an estimated ML Readiness Score.
    """

    score = 100

    # Missing values penalty
    total_cells = df.shape[0] * df.shape[1]
    total_missing = int(df.isnull().sum().sum())

    if total_cells > 0:

        missing_percentage = (
            total_missing / total_cells * 100
        )

        score -= missing_percentage * 0.7

    # Duplicate penalty
    if len(df) > 0:

        duplicate_percentage = (
            duplicate_info["duplicate_rows"]
            / len(df)
            * 100
        )

        score -= duplicate_percentage * 0.5

    # Constant columns
    score -= len(constant_columns) * 5

    # Outlier penalty
    for outlier in outliers:

        if outlier["outlier_percentage"] > 10:
            score -= 5

        elif outlier["outlier_percentage"] > 5:
            score -= 2

    # Very small datasets
    if len(df) < 50:
        score -= 10

    score = max(0, min(100, score))

    return round(float(score), 2)


def get_score_status(score):
    """
    Convert score into a readable status.
    """

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Good"

    if score >= 50:
        return "Needs Improvement"

    return "Poor"


def generate_recommendations(
    missing_issues,
    duplicate_info,
    constant_columns,
    high_cardinality_columns,
    outliers
):
    """
    Generate a list of overall recommendations.
    """

    recommendations = []

    if missing_issues:
        recommendations.append(
            "Handle missing values before performing machine learning."
        )

    if duplicate_info["duplicate_rows"] > 0:
        recommendations.append(
            "Remove duplicate rows from the dataset."
        )

    if constant_columns:
        recommendations.append(
            "Remove constant columns because they provide no predictive value."
        )

    if high_cardinality_columns:
        recommendations.append(
            "Review high-cardinality categorical columns before encoding them."
        )

    if outliers:
        recommendations.append(
            "Investigate detected outliers before training machine learning models."
        )

    if not recommendations:
        recommendations.append(
            "The dataset appears relatively clean and ready for further analysis."
        )

    return recommendations


def analyze_dataset(df):
    """
    Main AI Data Doctor analysis function.
    """

    missing_issues = detect_missing_values(df)

    duplicate_info = detect_duplicates(df)

    constant_columns = detect_constant_columns(df)

    high_cardinality_columns = (
        detect_high_cardinality_columns(df)
    )

    outliers = detect_outliers(df)

    data_types = detect_data_types(df)

    data_quality_score = calculate_data_quality_score(
        df,
        missing_issues,
        duplicate_info,
        constant_columns,
    )

    ml_readiness_score = calculate_ml_readiness_score(
        df,
        missing_issues,
        duplicate_info,
        constant_columns,
        outliers,
    )

    recommendations = generate_recommendations(
        missing_issues,
        duplicate_info,
        constant_columns,
        high_cardinality_columns,
        outliers,
    )

    return {
        "dataset_overview": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
        },

        "data_quality": {
            "score": data_quality_score,
            "status": get_score_status(
                data_quality_score
            ),
        },

        "ml_readiness": {
            "score": ml_readiness_score,
            "status": get_score_status(
                ml_readiness_score
            ),
        },

        "missing_values": missing_issues,

        "duplicates": duplicate_info,

        "constant_columns": constant_columns,

        "high_cardinality_columns": (
            high_cardinality_columns
        ),

        "outliers": outliers,

        "data_types": data_types,

        "recommendations": recommendations,
    }