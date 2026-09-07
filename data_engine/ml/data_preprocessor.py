import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from sklearn.compose import (
    ColumnTransformer
)

from sklearn.pipeline import (
    Pipeline
)

from sklearn.preprocessing import (
    OneHotEncoder
)

from sklearn.impute import (
    SimpleImputer
)

from sklearn.preprocessing import (
    StandardScaler
)


def identify_feature_types(
    dataframe
):
    """
    Identify numerical and categorical columns.
    """

    numerical_columns = (
        dataframe
        .select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    categorical_columns = (
        dataframe
        .select_dtypes(
            exclude=["number"]
        )
        .columns
        .tolist()
    )

    return (
        numerical_columns,
        categorical_columns
    )


def build_preprocessor(
    numerical_columns,
    categorical_columns
):
    """
    Build preprocessing pipeline.
    """

    numerical_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),

            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "numerical",
                numerical_pipeline,
                numerical_columns
            ),

            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            )
        ]
    )

    return preprocessor


def prepare_ml_data(
    dataframe,
    target_column,
    test_size=0.2,
    random_state=42
):
    """
    Prepare dataset for ML training.
    """

    working_dataframe = (
        dataframe.copy()
    )

    # Remove rows without target
    working_dataframe = (
        working_dataframe.dropna(
            subset=[target_column]
        )
    )

    X = working_dataframe.drop(
        columns=[target_column]
    )

    y = working_dataframe[
        target_column
    ]

    (
        numerical_columns,
        categorical_columns
    ) = identify_feature_types(X)

    preprocessor = build_preprocessor(

        numerical_columns,

        categorical_columns
    )

    X_train, X_test, y_train, y_test = (
        train_test_split(

            X,
            y,

            test_size=test_size,

            random_state=random_state
        )
    )

    return {

        "X_train": X_train,

        "X_test": X_test,

        "y_train": y_train,

        "y_test": y_test,

        "preprocessor":
            preprocessor,

        "numerical_columns":
            numerical_columns,

        "categorical_columns":
            categorical_columns
    }