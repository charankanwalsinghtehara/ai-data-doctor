import os

from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Dataset, AnalysisHistory
from .visualization_services import generate_visualizations

from .serializers import (
    DatasetSerializer,
    AnalysisHistorySerializer,
)

from .services import (
    analyze_dataset,
    clean_dataset,
)
from django.shortcuts import render


# =========================================================
# HOME
# =========================================================

@api_view(["GET"])
def home(request):

    return Response({
        "message": "AI Data Doctor Backend is running!",
        "status": "success",
        "version": "1.0",
    })


# =========================================================
# DATASET LIST + UPLOAD
# =========================================================

@api_view(["GET", "POST"])
def dataset_list_create(request):

    # GET ALL DATASETS
    if request.method == "GET":

        datasets = Dataset.objects.all().order_by(
            "-uploaded_at"
        )

        serializer = DatasetSerializer(
            datasets,
            many=True
        )

        return Response(serializer.data)

    # UPLOAD DATASET
    serializer = DatasetSerializer(
        data=request.data
    )

    if serializer.is_valid():

        dataset = serializer.save()

        if dataset.file:
            dataset.file_size = dataset.file.size
            dataset.save()

        return Response(
            DatasetSerializer(dataset).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# =========================================================
# DATASET DETAILS + DELETE
# =========================================================

@api_view(["GET", "DELETE"])
def dataset_detail(request, pk):

    try:

        dataset = Dataset.objects.get(pk=pk)

    except Dataset.DoesNotExist:

        return Response(
            {
                "error": "Dataset not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # GET DATASET
    if request.method == "GET":

        serializer = DatasetSerializer(
            dataset
        )

        return Response(
            serializer.data
        )

    # DELETE DATASET
    if request.method == "DELETE":

        # Delete physical file
        if dataset.file:

            dataset.file.delete(
                save=False
            )

        dataset.delete()

        return Response(
            {
                "message": (
                    "Dataset deleted successfully."
                )
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# COMPLETE DATASET ANALYSIS
# =========================================================

@api_view(["GET"])
def dataset_analysis(request, pk):

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

        analysis = analyze_dataset(
            dataset.file.path
        )

        # Save analysis history
        history = AnalysisHistory.objects.create(
            dataset=dataset,
            analysis_result=analysis
        )

        return Response({
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "analysis_id": history.id,
            "analysis": analysis,
        })

    except Exception as error:

        return Response(
            {
                "error": (
                    "Could not analyze dataset."
                ),
                "details": str(error),
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# AUTOMATIC DATA CLEANING
# =========================================================

@api_view(["POST"])
def dataset_clean(request, pk):

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

        result = clean_dataset(
            dataset.file.path
        )

        cleaned_df = result.pop(
            "dataframe"
        )

        # Create cleaned dataset directory
        cleaned_directory = os.path.join(
            settings.MEDIA_ROOT,
            "cleaned_datasets"
        )

        os.makedirs(
            cleaned_directory,
            exist_ok=True
        )

        # Cleaned filename
        cleaned_filename = (
            f"cleaned_dataset_{dataset.id}.csv"
        )

        cleaned_path = os.path.join(
            cleaned_directory,
            cleaned_filename
        )

        # Save cleaned dataset
        cleaned_df.to_csv(
            cleaned_path,
            index=False
        )

        cleaned_file_url = (
            request.build_absolute_uri(
                settings.MEDIA_URL
                + "cleaned_datasets/"
                + cleaned_filename
            )
        )

        return Response({
            "message": (
                "Dataset cleaned successfully."
            ),
            "dataset_id": dataset.id,
            "cleaned_file": cleaned_file_url,
            "cleaning_summary": result["summary"],
        })

    except Exception as error:

        return Response(
            {
                "error": (
                    "Could not clean dataset."
                ),
                "details": str(error),
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# DATASET INSIGHTS
# =========================================================

@api_view(["GET"])
def dataset_insights(request, pk):

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

        analysis = analyze_dataset(
            dataset.file.path
        )

        return Response({
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "data_quality": analysis[
                "data_quality"
            ],
            "insights": analysis[
                "insights"
            ],
            "recommendations": analysis[
                "cleaning_recommendations"
            ],
        })

    except Exception as error:

        return Response(
            {
                "error": (
                    "Could not generate insights."
                ),
                "details": str(error),
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================================================
# ANALYSIS HISTORY
# =========================================================

@api_view(["GET"])
def dataset_analysis_history(request, pk):

    try:

        dataset = Dataset.objects.get(pk=pk)

    except Dataset.DoesNotExist:

        return Response(
            {
                "error": "Dataset not found."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    history = dataset.analyses.all().order_by(
        "-created_at"
    )

    serializer = AnalysisHistorySerializer(
        history,
        many=True
    )

    return Response(serializer.data)


# =========================================================
# DATASET VISUALIZATIONS
# =========================================================

@api_view(["GET"])
def dataset_visualizations(request, pk):

    try:

        dataset = Dataset.objects.get(
            pk=pk
        )

    except Dataset.DoesNotExist:

        return Response(

            {
                "error": "Dataset not found."
            },

            status=status.HTTP_404_NOT_FOUND

        )


    try:

        result = generate_visualizations(

            file_path=dataset.file.path,

            dataset_id=dataset.id,

            request=request

        )


        return Response({

            "message": (
                "Visualizations generated successfully."
            ),

            "dataset_id": dataset.id,

            "dataset_name": dataset.name,

            "result": result,

        })


    except Exception as error:

        return Response(

            {

                "error": (
                    "Could not generate visualizations."
                ),

                "details": str(error),

            },

            status=status.HTTP_400_BAD_REQUEST

        )

def dashboard(request):

    return render(
        request,
        "data_doctor/dashboard.html"
    )