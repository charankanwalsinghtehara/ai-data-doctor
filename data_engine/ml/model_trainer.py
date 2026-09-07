from sklearn.pipeline import Pipeline


def get_classification_models():

    from sklearn.linear_model import (
        LogisticRegression
    )

    from sklearn.ensemble import (
        RandomForestClassifier
    )

    from sklearn.tree import (
        DecisionTreeClassifier
    )

    return {

        "LogisticRegression":
            LogisticRegression(
                max_iter=1000
            ),

        "RandomForestClassifier":
            RandomForestClassifier(
                random_state=42
            ),

        "DecisionTreeClassifier":
            DecisionTreeClassifier(
                random_state=42
            )
    }


def get_regression_models():

    from sklearn.linear_model import (
        LinearRegression
    )

    from sklearn.ensemble import (
        RandomForestRegressor
    )

    from sklearn.tree import (
        DecisionTreeRegressor
    )

    return {

        "LinearRegression":
            LinearRegression(),

        "RandomForestRegressor":
            RandomForestRegressor(
                random_state=42
            ),

        "DecisionTreeRegressor":
            DecisionTreeRegressor(
                random_state=42
            )
    }


def train_models(
    prepared_data,
    problem_type
):
    """
    Train multiple ML models.
    """

    if problem_type == "classification":

        models = (
            get_classification_models()
        )

    else:

        models = (
            get_regression_models()
        )

    trained_models = {}

    for model_name, model in (
        models.items()
    ):

        pipeline = Pipeline(

            steps=[

                (
                    "preprocessor",
                    prepared_data[
                        "preprocessor"
                    ]
                ),

                (
                    "model",
                    model
                )
            ]
        )

        try:

            pipeline.fit(

                prepared_data[
                    "X_train"
                ],

                prepared_data[
                    "y_train"
                ]
            )

            trained_models[
                model_name
            ] = {

                "success": True,

                "model":
                    pipeline
            }

        except Exception as error:

            trained_models[
                model_name
            ] = {

                "success": False,

                "error":
                    str(error)
            }

    return trained_models