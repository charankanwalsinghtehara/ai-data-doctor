from django.urls import path

from . import views

from .ml_views import (
    ml_dataset_analysis,
    train_ml_model,
    model_prediction,
    dataset_clustering,
    ml_model_history,
    ml_model_detail,
)


urlpatterns = [

    # =========================================================
    # HOME
    # =========================================================

    path("",views.home,name="home"),


    # =========================================================
    # DATASET MANAGEMENT
    # =========================================================

    # Dataset upload + list
    path("datasets/",views.dataset_list_create,name="dataset-list-create"),


    # Dataset detail + delete
    path("datasets/<int:pk>/",views.dataset_detail,name="dataset-detail"),


    # =========================================================
    # DATA ANALYSIS
    # =========================================================

    # Complete dataset analysis
    path("datasets/<int:pk>/analysis/",views.dataset_analysis,name="dataset-analysis"),


    # Dataset insights
    path("datasets/<int:pk>/insights/",views.dataset_insights,name="dataset-insights"),


    # Analysis history
    path("datasets/<int:pk>/history/",views.dataset_analysis_history,name="dataset-analysis-history"),


    # =========================================================
    # DATA CLEANING
    # =========================================================

    path("datasets/<int:pk>/clean/",views.dataset_clean,name="dataset-clean"),


    # =========================================================
    # DATA VISUALIZATION
    # =========================================================

    path("datasets/<int:pk>/visualizations/",views.dataset_visualizations,name="dataset-visualizations"),


    # =========================================================
    # MACHINE LEARNING
    # =========================================================

    # Analyze dataset for ML possibilities
    path("datasets/<int:pk>/ml-analysis/",ml_dataset_analysis,name="ml-dataset-analysis"),


    # Train classification or regression model
    path("datasets/<int:pk>/train-model/",train_ml_model,name="train-ml-model"),


    # Make predictions using trained model
    path("models/<int:pk>/predict/",model_prediction,name="model-prediction"),


    # Perform clustering
    path("datasets/<int:pk>/clustering/",dataset_clustering,name="dataset-clustering"),


    # View ML models created for a dataset
    path("datasets/<int:pk>/ml-models/",ml_model_history,name="ml-model-history"),


    # View individual ML model details
    path("models/<int:pk>/",ml_model_detail,name="ml-model-detail"),

]