import os
import json
import joblib

import numpy as np
import pandas as pd

from django.conf import settings

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler,
    LabelEncoder,
)

from sklearn.impute import SimpleImputer

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression,
)

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
)

from sklearn.tree import (
    DecisionTreeClassifier,
    DecisionTreeRegressor,
)

from sklearn.cluster import KMeans

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    silhouette_score,
)


# =========================================================
# DATASET LOADER
# =========================================================

def load_ml_dataset(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".csv":

        try:

            df = pd.read_csv(file_path)

        except UnicodeDecodeError:

            df = pd.read_csv(
                file_path,
                encoding="latin-1"
            )

    elif extension == ".xlsx":

        df = pd.read_excel(
            file_path,
            engine="openpyxl"
        )

    elif extension == ".xls":

        df = pd.read_excel(
            file_path,
            engine="xlrd"
        )

    else:

        raise ValueError(
            "Unsupported dataset format."
        )

    df.columns = df.columns.astype(str)

    return df


# =========================================================
# JSON SAFE CONVERSION
# =========================================================

def make_json_safe(value):

    if isinstance(value, dict):

        return {
            str(key): make_json_safe(val)
            for key, val in value.items()
        }

    if isinstance(value, list):

        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(
        value,
        (
            np.integer,
            np.int64,
            np.int32,
        )
    ):

        return int(value)

    if isinstance(
        value,
        (
            np.floating,
            np.float64,
            np.float32,
        )
    ):

        if np.isnan(value):

            return None

        return float(value)

    if isinstance(value, np.ndarray):

        return value.tolist()

    if pd.isna(value):

        return None

    return value


# =========================================================
# IDENTIFY COLUMN TYPES
# =========================================================

def identify_column_types(df):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=[
            "object",
            "category",
            "bool",
        ]
    ).columns.tolist()

    datetime_columns = df.select_dtypes(
        include=[
            "datetime",
            "datetimetz",
        ]
    ).columns.tolist()

    return {

        "numerical_columns": numerical_columns,

        "categorical_columns": categorical_columns,

        "datetime_columns": datetime_columns,

    }


# =========================================================
# DETECT POSSIBLE TARGET COLUMNS
# =========================================================

def detect_target_columns(df):

    possible_targets = []

    common_target_names = [

        "target",
        "label",
        "class",
        "outcome",
        "result",
        "response",
        "y",
        "status",
        "prediction",

    ]

    for column in df.columns:

        column_name = str(column).lower()

        unique_count = df[column].nunique(
            dropna=True
        )

        unique_percentage = (

            unique_count / len(df) * 100

            if len(df) > 0

            else 0

        )

        score = 0

        reasons = []

        if column_name in common_target_names:

            score += 5

            reasons.append(
                "Column name commonly used as a target."
            )

        if any(
            word in column_name
            for word in common_target_names
        ):

            score += 2

            reasons.append(
                "Column name suggests prediction output."
            )

        if unique_count <= 20:

            score += 2

            reasons.append(
                "Low number of unique values."
            )

        if (
            df[column].dtype == "object"
            or
            df[column].dtype == "bool"
        ):

            score += 2

            reasons.append(
                "Categorical column suitable for classification."
            )

        if unique_percentage > 90:

            score -= 2

            reasons.append(
                "Very high uniqueness may indicate an ID column."
            )

        if "id" in column_name:

            score -= 3

            reasons.append(
                "Column appears to be an identifier."
            )

        possible_targets.append({

            "column": column,

            "score": score,

            "unique_values": int(unique_count),

            "reasons": reasons,

        })

    possible_targets.sort(

        key=lambda item: item["score"],

        reverse=True

    )

    return possible_targets


# =========================================================
# DETECT ML PROBLEM TYPE
# =========================================================

def detect_problem_type(df, target_column=None):

    if target_column is None:

        return {

            "problem_type": "unknown",

            "message": (
                "No target column selected. "
                "Dataset may be used for clustering."
            ),

        }

    if target_column not in df.columns:

        raise ValueError(
            "Selected target column does not exist."
        )

    target = df[target_column].dropna()

    if len(target) == 0:

        raise ValueError(
            "Target column contains no usable values."
        )

    unique_count = target.nunique()

    total_count = len(target)

    if (
        target.dtype == "object"
        or
        target.dtype == "bool"
        or
        str(target.dtype) == "category"
    ):

        return {

            "problem_type": "classification",

            "reason": (
                "Target column is categorical."
            ),

            "unique_values": int(unique_count),

        }

    if unique_count <= 20:

        return {

            "problem_type": "classification",

            "reason": (
                "Target column has a small number "
                "of unique values."
            ),

            "unique_values": int(unique_count),

        }

    if unique_count / total_count < 0.05:

        return {

            "problem_type": "classification",

            "reason": (
                "Target column has relatively few "
                "unique values."
            ),

            "unique_values": int(unique_count),

        }

    return {

        "problem_type": "regression",

        "reason": (
            "Target column is numerical with many "
            "unique values."
        ),

        "unique_values": int(unique_count),

    }


# =========================================================
# ML READINESS ANALYSIS
# =========================================================

def analyze_ml_readiness(file_path):

    df = load_ml_dataset(file_path)

    rows, columns = df.shape

    column_types = identify_column_types(df)

    possible_targets = detect_target_columns(df)

    missing_percentage = round(

        (
            df.isnull().sum().sum()
            /
            (rows * columns)
            * 100
        ),

        2

    ) if rows > 0 and columns > 0 else 0

    duplicate_percentage = round(

        (
            df.duplicated().sum()
            /
            rows
            * 100
        ),

        2

    ) if rows > 0 else 0

    score = 100

    warnings = []

    recommendations = []

    if rows < 50:

        score -= 20

        warnings.append(
            "Dataset has fewer than 50 rows."
        )

    elif rows < 100:

        score -= 10

        warnings.append(
            "Dataset has limited training data."
        )

    if columns < 2:

        score -= 30

        warnings.append(
            "Dataset has too few columns."
        )

    if missing_percentage > 20:

        score -= 15

        warnings.append(
            "Dataset contains many missing values."
        )

    if duplicate_percentage > 10:

        score -= 10

        warnings.append(
            "Dataset contains many duplicate rows."
        )

    score = max(0, score)

    if score >= 85:

        readiness = "Excellent"

    elif score >= 70:

        readiness = "Good"

    elif score >= 50:

        readiness = "Moderate"

    else:

        readiness = "Poor"

    recommendations.append(
        "Review and select an appropriate target column."
    )

    recommendations.append(
        "Remove identifier columns before training."
    )

    recommendations.append(
        "Review missing values before model training."
    )

    return make_json_safe({

        "dataset_summary": {

            "rows": rows,

            "columns": columns,

        },

        "column_types": column_types,

        "possible_target_columns": possible_targets[:10],

        "data_issues": {

            "missing_percentage": missing_percentage,

            "duplicate_percentage": duplicate_percentage,

        },

        "ml_readiness": {

            "score": score,

            "level": readiness,

        },

        "warnings": warnings,

        "recommendations": recommendations,

    })


# =========================================================
# PREPARE FEATURES
# =========================================================

def prepare_features(df, target_column):

    if target_column not in df.columns:

        raise ValueError(
            "Target column does not exist."
        )

    df = df.copy()

    df = df.dropna(
        subset=[target_column]
    )

    X = df.drop(
        columns=[target_column]
    )

    y = df[target_column]

    # Remove completely empty columns
    empty_columns = [

        column

        for column in X.columns

        if X[column].isnull().all()

    ]

    if empty_columns:

        X = X.drop(
            columns=empty_columns
        )

    # Remove ID-like columns
    columns_to_remove = []

    for column in X.columns:

        column_name = str(column).lower()

        unique_ratio = (

            X[column].nunique()
            /
            len(X)

            if len(X) > 0

            else 0

        )

        if (
            column_name == "id"
            or
            column_name.endswith("_id")
            or
            unique_ratio > 0.98
        ):

            columns_to_remove.append(
                column
            )

    if columns_to_remove:

        X = X.drop(
            columns=columns_to_remove
        )

    numerical_columns = X.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = X.select_dtypes(

        include=[
            "object",
            "category",
            "bool",
        ]

    ).columns.tolist()

    # Convert datetime columns to numeric timestamps
    datetime_columns = X.select_dtypes(

        include=[
            "datetime",
            "datetimetz",
        ]

    ).columns.tolist()

    for column in datetime_columns:

        X[column] = pd.to_datetime(
            X[column],
            errors="coerce"
        )

        X[column] = (
            X[column]
            .astype("int64")
            .replace(
                -9223372036854775808,
                np.nan
            )
        )

        numerical_columns.append(
            column
        )

    return {

        "X": X,

        "y": y,

        "numerical_columns": numerical_columns,

        "categorical_columns": categorical_columns,

        "removed_columns": columns_to_remove
        + empty_columns,

    }


# =========================================================
# CREATE PREPROCESSOR
# =========================================================

def create_preprocessor(

    numerical_columns,
    categorical_columns

):

    transformers = []

    if numerical_columns:

        numerical_pipeline = Pipeline([

            (
                "imputer",

                SimpleImputer(
                    strategy="median"
                ),

            ),

            (
                "scaler",

                StandardScaler(),

            ),

        ])

        transformers.append(

            (
                "numerical",

                numerical_pipeline,

                numerical_columns,

            )

        )

    if categorical_columns:

        categorical_pipeline = Pipeline([

            (
                "imputer",

                SimpleImputer(
                    strategy="most_frequent"
                ),

            ),

            (
                "encoder",

                OneHotEncoder(
                    handle_unknown="ignore"
                ),

            ),

        ])

        transformers.append(

            (
                "categorical",

                categorical_pipeline,

                categorical_columns,

            )

        )

    if not transformers:

        raise ValueError(
            "No usable feature columns found."
        )

    return ColumnTransformer(
        transformers=transformers
    )


# =========================================================
# CLASSIFICATION TRAINING
# =========================================================

def train_classification_models(

    X,
    y,
    preprocessor

):

    if y.nunique() < 2:

        raise ValueError(
            "Classification requires at least "
            "two target classes."
        )

    label_encoder = LabelEncoder()

    y_encoded = label_encoder.fit_transform(
        y.astype(str)
    )

    class_counts = pd.Series(
        y_encoded
    ).value_counts()

    stratify_data = None

    if class_counts.min() >= 2:

        stratify_data = y_encoded

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,

            y_encoded,

            test_size=0.2,

            random_state=42,

            stratify=stratify_data,

        )

    )

    models = {

        "Logistic Regression":

            LogisticRegression(
                max_iter=2000
            ),

        "Decision Tree":

            DecisionTreeClassifier(
                random_state=42
            ),

        "Random Forest":

            RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
            ),

    }

    results = {}

    trained_pipelines = {}

    for model_name, model in models.items():

        pipeline = Pipeline([

            (
                "preprocessor",
                preprocessor,
            ),

            (
                "model",
                model,
            ),

        ])

        pipeline.fit(
            X_train,
            y_train
        )

        predictions = pipeline.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0,

        )

        recall = recall_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0,

        )

        f1 = f1_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0,

        )

        results[model_name] = {

            "accuracy": round(
                float(accuracy),
                4
            ),

            "precision": round(
                float(precision),
                4
            ),

            "recall": round(
                float(recall),
                4
            ),

            "f1_score": round(
                float(f1),
                4
            ),

        }

        trained_pipelines[model_name] = pipeline

    best_model_name = max(

        results,

        key=lambda name:
            results[name]["accuracy"]

    )

    return {

        "problem_type": "classification",

        "results": results,

        "best_model_name": best_model_name,

        "best_model": trained_pipelines[
            best_model_name
        ],

        "label_encoder": label_encoder,

        "X_test": X_test,

        "y_test": y_test,

        "predictions": trained_pipelines[
            best_model_name
        ].predict(X_test),

    }


# =========================================================
# REGRESSION TRAINING
# =========================================================

def train_regression_models(

    X,
    y,
    preprocessor

):

    y_numeric = pd.to_numeric(
        y,
        errors="coerce"
    )

    valid_rows = y_numeric.notna()

    X = X.loc[valid_rows]

    y_numeric = y_numeric.loc[
        valid_rows
    ]

    if len(y_numeric) < 10:

        raise ValueError(
            "Not enough valid rows for regression."
        )

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,

            y_numeric,

            test_size=0.2,

            random_state=42,

        )

    )

    models = {

        "Linear Regression":

            LinearRegression(),

        "Decision Tree":

            DecisionTreeRegressor(
                random_state=42
            ),

        "Random Forest":

            RandomForestRegressor(

                n_estimators=200,

                random_state=42,

                n_jobs=-1,

            ),

    }

    results = {}

    trained_pipelines = {}

    for model_name, model in models.items():

        pipeline = Pipeline([

            (
                "preprocessor",
                preprocessor,
            ),

            (
                "model",
                model,
            ),

        ])

        pipeline.fit(
            X_train,
            y_train
        )

        predictions = pipeline.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        mse = mean_squared_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(mse)

        r2 = r2_score(
            y_test,
            predictions
        )

        results[model_name] = {

            "mae": round(
                float(mae),
                4
            ),

            "mse": round(
                float(mse),
                4
            ),

            "rmse": round(
                float(rmse),
                4
            ),

            "r2_score": round(
                float(r2),
                4
            ),

        }

        trained_pipelines[model_name] = pipeline

    best_model_name = max(

        results,

        key=lambda name:
            results[name]["r2_score"]

    )

    return {

        "problem_type": "regression",

        "results": results,

        "best_model_name": best_model_name,

        "best_model": trained_pipelines[
            best_model_name
        ],

        "X_test": X_test,

        "y_test": y_test,

        "predictions": trained_pipelines[
            best_model_name
        ].predict(X_test),

    }


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

def get_feature_importance(

    pipeline

):

    try:

        model = pipeline.named_steps[
            "model"
        ]

        preprocessor = pipeline.named_steps[
            "preprocessor"
        ]

        if not hasattr(
            model,
            "feature_importances_"
        ):

            return []

        feature_names = (
            preprocessor.get_feature_names_out()
        )

        importance_values = (
            model.feature_importances_
        )

        importance_data = []

        for feature, importance in zip(

            feature_names,

            importance_values

        ):

            importance_data.append({

                "feature": str(feature),

                "importance": round(
                    float(importance),
                    6
                ),

            })

        importance_data.sort(

            key=lambda item:
                item["importance"],

            reverse=True

        )

        return importance_data[:20]

    except Exception:

        return []


# =========================================================
# SAVE TRAINED MODEL
# =========================================================

def save_trained_model(

    model,

    dataset_id,

    target_column,

    problem_type,

    feature_columns,

    label_encoder=None,

):

    models_directory = os.path.join(

        settings.MEDIA_ROOT,

        "trained_models"

    )

    os.makedirs(

        models_directory,

        exist_ok=True

    )

    model_filename = (

        f"dataset_{dataset_id}_"
        f"{problem_type}_"
        f"model.joblib"

    )

    model_path = os.path.join(

        models_directory,

        model_filename

    )

    model_data = {

        "model": model,

        "target_column": target_column,

        "problem_type": problem_type,

        "feature_columns": feature_columns,

        "label_encoder": label_encoder,

    }

    joblib.dump(

        model_data,

        model_path

    )

    return {

        "model_path": model_path,

        "model_filename": model_filename,

    }


# =========================================================
# COMPLETE MODEL TRAINING
# =========================================================

def train_dataset_model(

    file_path,

    dataset_id,

    target_column,

):

    df = load_ml_dataset(file_path)

    if len(df) < 10:

        raise ValueError(
            "Dataset must contain at least "
            "10 rows for training."
        )

    problem_info = detect_problem_type(

        df,

        target_column

    )

    problem_type = problem_info[
        "problem_type"
    ]

    prepared_data = prepare_features(

        df,

        target_column

    )

    X = prepared_data["X"]

    y = prepared_data["y"]

    if X.shape[1] == 0:

        raise ValueError(
            "No usable features available "
            "for model training."
        )

    preprocessor = create_preprocessor(

        prepared_data[
            "numerical_columns"
        ],

        prepared_data[
            "categorical_columns"
        ],

    )

    if problem_type == "classification":

        training_result = (

            train_classification_models(

                X,

                y,

                preprocessor

            )

        )

    elif problem_type == "regression":

        training_result = (

            train_regression_models(

                X,

                y,

                preprocessor

            )

        )

    else:

        raise ValueError(
            "Unsupported ML problem type."
        )

    best_model = training_result[
        "best_model"
    ]

    feature_importance = get_feature_importance(
        best_model
    )

    model_save_result = save_trained_model(

        model=best_model,

        dataset_id=dataset_id,

        target_column=target_column,

        problem_type=problem_type,

        feature_columns=X.columns.tolist(),

        label_encoder=training_result.get(
            "label_encoder"
        ),

    )

    return make_json_safe({

        "problem_type": problem_type,

        "problem_detection": problem_info,

        "target_column": target_column,

        "features_used": X.columns.tolist(),

        "removed_columns": prepared_data[
            "removed_columns"
        ],

        "model_results": training_result[
            "results"
        ],

        "best_model": training_result[
            "best_model_name"
        ],

        "feature_importance": feature_importance,

        "model_file": model_save_result[
            "model_filename"
        ],

        "model_path": model_save_result[
            "model_path"
        ],

    })


# =========================================================
# LOAD TRAINED MODEL
# =========================================================

def load_trained_model(model_path):

    if not os.path.exists(model_path):

        raise ValueError(
            "Trained model file not found."
        )

    return joblib.load(model_path)


# =========================================================
# MAKE PREDICTIONS
# =========================================================

def predict_with_model(

    model_path,

    input_data

):

    model_data = load_trained_model(
        model_path
    )

    model = model_data["model"]

    feature_columns = model_data[
        "feature_columns"
    ]

    problem_type = model_data[
        "problem_type"
    ]

    label_encoder = model_data.get(
        "label_encoder"
    )

    if isinstance(input_data, dict):

        input_df = pd.DataFrame([
            input_data
        ])

    elif isinstance(input_data, list):

        input_df = pd.DataFrame(
            input_data
        )

    else:

        raise ValueError(
            "Input data must be a dictionary "
            "or a list of dictionaries."
        )

    missing_columns = [

        column

        for column in feature_columns

        if column not in input_df.columns

    ]

    if missing_columns:

        raise ValueError(

            "Missing required features: "

            + ", ".join(missing_columns)

        )

    input_df = input_df[
        feature_columns
    ]

    predictions = model.predict(
        input_df
    )

    if (
        problem_type == "classification"
        and label_encoder is not None
    ):

        predictions = (
            label_encoder.inverse_transform(
                predictions.astype(int)
            )
        )

    return make_json_safe({

        "problem_type": problem_type,

        "target_column": model_data[
            "target_column"
        ],

        "predictions": predictions,

    })


# =========================================================
# CLUSTERING
# =========================================================

def perform_clustering(

    file_path,

    n_clusters=3

):

    df = load_ml_dataset(file_path)

    numerical_df = df.select_dtypes(
        include=["number"]
    ).copy()

    numerical_df = numerical_df.dropna()

    if numerical_df.shape[1] < 2:

        raise ValueError(
            "Clustering requires at least "
            "two numerical columns."
        )

    if len(numerical_df) < n_clusters:

        raise ValueError(
            "Not enough rows for clustering."
        )

    scaler = StandardScaler()

    scaled_data = scaler.fit_transform(
        numerical_df
    )

    model = KMeans(

        n_clusters=n_clusters,

        random_state=42,

        n_init=10,

    )

    cluster_labels = model.fit_predict(
        scaled_data
    )

    silhouette = None

    if (
        n_clusters > 1
        and len(set(cluster_labels)) > 1
        and len(numerical_df) > n_clusters
    ):

        silhouette = silhouette_score(

            scaled_data,

            cluster_labels

        )

    cluster_counts = pd.Series(
        cluster_labels
    ).value_counts().sort_index()

    return make_json_safe({

        "n_clusters": n_clusters,

        "numerical_features": numerical_df.columns.tolist(),

        "cluster_counts": {

            str(cluster): int(count)

            for cluster, count
            in cluster_counts.items()

        },

        "silhouette_score": (

            round(
                float(silhouette),
                4
            )

            if silhouette is not None

            else None

        ),

    })