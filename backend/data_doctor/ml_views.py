from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Dataset,
    MLModelHistory,
)

from .serializers import (
    MLModelHistorySerializer,
)

from .ml_services import (

    analyze_ml_readiness,

    train_dataset_model,

    predict_with_model,

    perform_clustering,

)


# =========================================================
# ML READINESS ANALYSIS
# =========================================================

@api_view(["GET"])
def ml_dataset_analysis(request, pk):

    try:

        dataset = Dataset.objects.get(pk=pk)

    except Dataset.DoesNotExist:

        return Response(

            {
                "error": "Dataset not found."
            },

            status=status.HTTP_404_NOT_FOUND

        )

    try:

        result = analyze_ml_readiness(
            dataset.file.path
        )

        return Response({

            "message": (
                "ML readiness analysis completed."
            ),

            "dataset_id": dataset.id,

            "dataset_name": dataset.name,

            "ml_analysis": result,

        })

    except Exception as error:

        return Response(

            {

                "error": (
                    "Could not analyze dataset "
                    "for machine learning."
                ),

                "details": str(error),

            },

            status=status.HTTP_400_BAD_REQUEST

        )


# =========================================================
# TRAIN MODEL
# =========================================================

@api_view(["POST"])
def train_ml_model(request, pk):

    try:

        dataset = Dataset.objects.get(pk=pk)

    except Dataset.DoesNotExist:

        return Response(

            {
                "error": "Dataset not found."
            },

            status=status.HTTP_404_NOT_FOUND

        )

    target_column = request.data.get(
        "target_column"
    )

    if not target_column:

        return Response(

            {
                "error": (
                    "target_column is required."
                )
            },

            status=status.HTTP_400_BAD_REQUEST

        )

    try:

        result = train_dataset_model(

            file_path=dataset.file.path,

            dataset_id=dataset.id,

            target_column=target_column,

        )

        history = MLModelHistory.objects.create(

            dataset=dataset,

            target_column=target_column,

            problem_type=result[
                "problem_type"
            ],

            best_model=result[
                "best_model"
            ],

            model_results=result[
                "model_results"
            ],

            feature_importance=result[
                "feature_importance"
            ],

            model_file=result[
                "model_path"
            ],

        )

        return Response({

            "message": (
                "Model training completed "
                "successfully."
            ),

            "training_id": history.id,

            "dataset_id": dataset.id,

            "dataset_name": dataset.name,

            "training_result": result,

        })

    except Exception as error:

        return Response(

            {

                "error": (
                    "Could not train model."
                ),

                "details": str(error),

            },

            status=status.HTTP_400_BAD_REQUEST

        )


# =========================================================
# MODEL PREDICTION
# =========================================================

@api_view(["POST"])
def model_prediction(request, pk):

    try:

        model_history = (
            MLModelHistory.objects.get(pk=pk)
        )

    except MLModelHistory.DoesNotExist:

        return Response(

            {
                "error": "Trained model not found."
            },

            status=status.HTTP_404_NOT_FOUND

        )

    input_data = request.data.get(
        "input_data"
    )

    if input_data is None:

        return Response(

            {
                "error": (
                    "input_data is required."
                )
            },

            status=status.HTTP_400_BAD_REQUEST

        )

    try:

        result = predict_with_model(

            model_path=model_history.model_file,

            input_data=input_data,

        )

        return Response({

            "message": (
                "Prediction completed successfully."
            ),

            "model_id": model_history.id,

            "model_name": model_history.best_model,

            "result": result,

        })

    except Exception as error:

        return Response(

            {

                "error": (
                    "Could not make prediction."
                ),

                "details": str(error),

            },

            status=status.HTTP_400_BAD_REQUEST

        )


# =========================================================
# CLUSTERING
# =========================================================

@api_view(["POST"])
def dataset_clustering(request, pk):

    try:

        dataset = Dataset.objects.get(pk=pk)

    except Dataset.DoesNotExist:

        return Response(

            {
                "error": "Dataset not found."
            },

            status=status.HTTP_404_NOT_FOUND

        )

    n_clusters = request.data.get(
        "n_clusters",
        3
    )

    try:

        n_clusters = int(n_clusters)

        if n_clusters < 2:

            raise ValueError

    except ValueError:

        return Response(

            {
                "error": (
                    "n_clusters must be "
                    "an integer greater than 1."
                )
            },

            status=status.HTTP_400_BAD_REQUEST

        )

    try:

        result = perform_clustering(

            file_path=dataset.file.path,

            n_clusters=n_clusters,

        )

        return Response({

            "message": (
                "Clustering completed successfully."
            ),

            "dataset_id": dataset.id,

            "dataset_name": dataset.name,

            "clustering_result": result,

        })

    except Exception as error:

        return Response(

            {

                "error": (
                    "Could not perform clustering."
                ),

                "details": str(error),

            },

            status=status.HTTP_400_BAD_REQUEST

        )


# =========================================================
# ML MODEL HISTORY
# =========================================================

@api_view(["GET"])
def ml_model_history(request, pk):

    try:

        dataset = Dataset.objects.get(pk=pk)

    except Dataset.DoesNotExist:

        return Response(

            {
                "error": "Dataset not found."
            },

            status=status.HTTP_404_NOT_FOUND

        )

    models = dataset.ml_models.all().order_by(
        "-created_at"
    )

    serializer = MLModelHistorySerializer(

        models,

        many=True

    )

    return Response(serializer.data)


# =========================================================
# MODEL DETAILS
# =========================================================

@api_view(["GET", "DELETE"])
def ml_model_detail(request, pk):

    try:

        model_history = (
            MLModelHistory.objects.get(pk=pk)
        )

    except MLModelHistory.DoesNotExist:

        return Response(

            {
                "error": "Model not found."
            },

            status=status.HTTP_404_NOT_FOUND

        )

    if request.method == "GET":

        serializer = MLModelHistorySerializer(
            model_history
        )

        return Response(serializer.data)

    if request.method == "DELETE":

        model_file = model_history.model_file

        model_history.delete()

        return Response({

            "message": (
                "Model history deleted successfully."
            ),

            "deleted_model_file": model_file,

        })