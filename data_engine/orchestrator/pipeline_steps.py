
import pandas as pd


# ==========================================
# VALIDATION
# ==========================================

from data_engine.validation import (
    run_file_validation,
    run_dataset_validation
)


def run_file_validation_step(file_path):

    return run_file_validation(
        file_path
    )


def run_dataset_validation_step(dataframe):

    return run_dataset_validation(
        dataframe
    )


# ==========================================
# INGESTION
# ==========================================

from data_engine.ingestion import (
    ingest_file
)


def run_ingestion_step(file_path):

    return ingest_file(
        file_path
    )


# ==========================================
# EXTRACTION
# ==========================================

from data_engine.extraction import (
    extract_data
)


def run_extraction_step(
    file_path,
    ingestion_result
):

    file_info = ingestion_result.get(
        "file_info",
        ingestion_result
    )


    return extract_data(

        file_path,

        file_info
    )


# ==========================================
# DATAFRAME VALIDATION
# ==========================================

def validate_dataframe(dataframe):

    if not isinstance(
        dataframe,
        pd.DataFrame
    ):

        raise TypeError(
            "Expected a Pandas DataFrame."
        )


    if dataframe.empty:

        raise ValueError(
            "Dataset is empty."
        )


    return True


# ==========================================
# METADATA
# ==========================================

from data_engine.metadata import (
    run_metadata_engine
)


def run_metadata_step(

    file_path,

    dataframe,

    project_id=None,

    project_name=None
):

    return run_metadata_engine(

        file_path=file_path,

        dataframe=dataframe,

        project_id=project_id,

        project_name=project_name
    )


# ==========================================
# UNDERSTANDING
# ==========================================

from data_engine.understanding import (
    understand_dataset
)


def run_understanding_step(dataframe):

    return understand_dataset(
        dataframe
    )


# ==========================================
# PROFILING
# ==========================================

from data_engine.profiling import (
    profile_dataset_complete
)


def run_profiling_step(

    dataframe,

    understanding_result
):

    return profile_dataset_complete(

        dataframe,

        understanding_result
    )


# ==========================================
# QUALITY
# ==========================================

from data_engine.quality import (
    check_data_quality
)


def run_quality_step(

    dataframe,

    understanding_result
):

    return check_data_quality(

        dataframe,

        understanding_result
    )


# ==========================================
# CLEANING
# ==========================================

from data_engine.cleaning import (
    clean_dataset
)


def run_cleaning_step(

    dataframe,

    understanding_result,

    quality_result,

    auto_clean=True
):

    return clean_dataset(

        dataframe,

        understanding_result,

        quality_result,

        auto_clean
    )


# ==========================================
# PREPROCESSING
# ==========================================

from data_engine.preprocessing import (
    run_preprocessing_engine
)


def run_preprocessing_step(

    dataframe,

    scale_data=False
):

    return run_preprocessing_engine(

        dataframe,

        scale_data=scale_data
    )


# ==========================================
# ANALYSIS
# ==========================================

from data_engine.analysis import (
    analyze_dataset
)


def run_analysis_step(

    dataframe,

    understanding_result
):

    return analyze_dataset(

        dataframe,

        understanding_result
    )


# ==========================================
# ANOMALY DETECTION
# ==========================================

from data_engine.anomaly import (
    detect_anomalies
)


def run_anomaly_step(dataframe):

    return detect_anomalies(
        dataframe
    )


# ==========================================
# MACHINE LEARNING
# ==========================================

from data_engine.ml import (

    get_ml_recommendations,

    train_ml_pipeline
)


def run_ml_recommendation_step(
    dataframe
):

    return get_ml_recommendations(
        dataframe
    )


def run_ml_training_step(

    dataframe,

    target_column,

    save_best_model=True
):

    return train_ml_pipeline(

        dataframe,

        target_column,

        save_best_model
    )


# ==========================================
# INTELLIGENCE
# ==========================================

from data_engine.intelligence import (
    run_intelligence_engine
)


def run_intelligence_step(

    dataframe,

    previous_results=None
):

    return run_intelligence_engine(

        dataframe,

        previous_results
    )


# ==========================================
# VISUALIZATION
# ==========================================

from data_engine.visualization import (
    run_visualization_engine
)


def run_visualization_step(

    dataframe,

    project_id
):

    return run_visualization_engine(

        dataframe,

        project_id
    )


# ==========================================
# REPORTING
# ==========================================

from data_engine.reporting import (
    generate_report
)


def run_reporting_step(

    dataframe,

    understanding_result=None,

    profiling_result=None,

    quality_result=None,

    cleaning_result=None,

    analysis_result=None,

    anomaly_result=None,

    ml_recommendations=None,

    ml_result=None
):

    return generate_report(

        dataframe=dataframe,

        understanding_result=
            understanding_result,

        profiling_result=
            profiling_result,

        quality_result=
            quality_result,

        cleaning_result=
            cleaning_result,

        analysis_result=
            analysis_result,

        anomaly_result=
            anomaly_result,

        ml_recommendations=
            ml_recommendations,

        ml_result=
            ml_result
    )


# ==========================================
# MONITORING
# ==========================================

from data_engine.monitoring import (
    MonitoringEngine
)


def create_monitoring_engine():

    return MonitoringEngine()

