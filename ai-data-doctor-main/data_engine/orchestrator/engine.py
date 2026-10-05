
from .pipeline_config import (
    create_pipeline_config
)

from .pipeline_state import (
    PipelineState
)

from .pipeline_steps import (

    validate_dataframe,

    run_file_validation_step,
    run_dataset_validation_step,

    run_ingestion_step,
    run_extraction_step,

    run_metadata_step,

    run_understanding_step,
    run_profiling_step,
    run_quality_step,
    run_cleaning_step,

    run_analysis_step,
    run_anomaly_step,

    run_ml_recommendation_step,

    run_intelligence_step,

    run_reporting_step,
    run_visualization_step,

    create_monitoring_engine
)

from .exceptions import (
    PipelineStepError
)


# =========================================================
# STORAGE
# =========================================================

from data_engine.storage import (
    create_data_project,
    save_project_results
)


# =========================================================
# CACHE
# =========================================================

from data_engine.cache import (
    get_cached_result,
    save_cached_result
)


# =========================================================
# LOGGING
# =========================================================

from data_engine.logging import (

    log_pipeline_start,

    log_step_start,
    log_step_complete,
    log_step_failed,

    log_pipeline_complete,
    log_pipeline_failed
)


# =========================================================
# SAFE STEP EXECUTOR
# =========================================================

def execute_step(

    state,

    step_name,

    function,

    monitor=None,

    *args,

    **kwargs
):

    """
    Execute one pipeline step safely.
    """


    state.start_step(
        step_name
    )


    log_step_start(
        step_name
    )


    step_monitor = None


    if monitor is not None:

        step_monitor = (
            monitor.start_step(
                step_name
            )
        )


    try:

        result = function(

            *args,

            **kwargs
        )


        state.complete_step(
            step_name
        )


        log_step_complete(
            step_name
        )


        if step_monitor is not None:

            monitor.complete_step(
                step_monitor
            )


        return result


    except Exception as error:


        state.fail_step(

            step_name,

            error
        )


        log_step_failed(

            step_name,

            error
        )


        if step_monitor is not None:

            monitor.complete_step(
                step_monitor
            )


        raise PipelineStepError(

            step_name,

            error
        )


# =========================================================
# MAIN AI DATA DOCTOR PIPELINE
# =========================================================

def run_ai_data_doctor(

    file_path,

    project_name=None,

    config=None
):

    """
    Run the complete
    AI Data Doctor pipeline.
    """


    # =====================================================
    # CONFIGURATION
    # =====================================================

    pipeline_config = (

        create_pipeline_config(
            config
        )
    )


    # =====================================================
    # PIPELINE STATE
    # =====================================================

    state = PipelineState()


    # =====================================================
    # RESULTS
    # =====================================================

    results = {}


    # =====================================================
    # PIPELINE START
    # =====================================================

    log_pipeline_start(
        project_name
    )


    # =====================================================
    # MONITORING
    # =====================================================

    monitor = None


    if pipeline_config.get(
        "run_monitoring",
        True
    ):

        monitor = (
            create_monitoring_engine()
        )

        monitor.start_pipeline()


    try:


        # =================================================
        # CACHE CHECK
        # =================================================

        if pipeline_config.get(
            "run_cache",
            True
        ):


            cached_result = (

                get_cached_result(
                    file_path
                )
            )


            if cached_result is not None:


                cached_data = (
                    cached_result["data"]
                )


                cached_data[
                    "from_cache"
                ] = True


                return cached_data


        # =================================================
        # CREATE PROJECT
        # =================================================

        project = (

            create_data_project(
                project_name
            )
        )


        project_id = project.get(
            "project_id"
        )


        results[
            "project"
        ] = project


        # =================================================
        # FILE VALIDATION
        # =================================================

        if pipeline_config.get(
            "run_validation",
            True
        ):


            results[
                "file_validation"
            ] = execute_step(

                state,

                "file_validation",

                run_file_validation_step,

                monitor,

                file_path
            )


        # =================================================
        # INGESTION
        # =================================================

        ingestion_result = (

            execute_step(

                state,

                "ingestion",

                run_ingestion_step,

                monitor,

                file_path
            )
        )


        results[
            "ingestion"
        ] = ingestion_result


        # =================================================
        # EXTRACTION
        # =================================================

        extraction_result = (

            execute_step(

                state,

                "extraction",

                run_extraction_step,

                monitor,

                file_path,

                ingestion_result
            )
        )


        results[
            "extraction"
        ] = extraction_result


        # =================================================
        # GET DATAFRAME
        # =================================================

        dataframe = extraction_result.get(
            "data"
        )


        # Backup support

        if dataframe is None:

            dataframe = extraction_result.get(
                "dataframe"
            )


        # =================================================
        # DATAFRAME VALIDATION
        # =================================================

        validate_dataframe(
            dataframe
        )


        # =================================================
        # KEEP ORIGINAL DATA SAFE
        # =================================================

        original_dataframe = (
            dataframe.copy()
        )


        # =================================================
        # METADATA
        # =================================================

        if pipeline_config.get(
            "run_metadata",
            True
        ):


            results[
                "metadata"
            ] = execute_step(

                state,

                "metadata",

                run_metadata_step,

                monitor,

                file_path,

                dataframe,

                project_id,

                project_name
            )


        # =================================================
        # DATASET VALIDATION
        # =================================================

        if pipeline_config.get(
            "run_validation",
            True
        ):


            results[
                "dataset_validation"
            ] = execute_step(

                state,

                "dataset_validation",

                run_dataset_validation_step,

                monitor,

                dataframe
            )


        # =================================================
        # UNDERSTANDING
        # =================================================

        understanding_result = None


        if pipeline_config.get(
            "run_understanding",
            True
        ):


            understanding_result = (

                execute_step(

                    state,

                    "understanding",

                    run_understanding_step,

                    monitor,

                    dataframe
                )
            )


            results[
                "understanding"
            ] = understanding_result


        # =================================================
        # PROFILING
        # =================================================

        profiling_result = None


        if pipeline_config.get(
            "run_profiling",
            True
        ):


            profiling_result = (

                execute_step(

                    state,

                    "profiling",

                    run_profiling_step,

                    monitor,

                    dataframe,

                    understanding_result
                )
            )


            results[
                "profiling"
            ] = profiling_result


        # =================================================
        # QUALITY
        # =================================================

        quality_result = None


        if pipeline_config.get(
            "run_quality",
            True
        ):


            quality_result = (

                execute_step(

                    state,

                    "quality",

                    run_quality_step,

                    monitor,

                    dataframe,

                    understanding_result
                )
            )


            results[
                "quality"
            ] = quality_result


        # =================================================
        # CLEANING
        # =================================================

        cleaned_dataframe = (
            dataframe.copy()
        )


        cleaning_result = None


        if pipeline_config.get(
            "run_cleaning",
            True
        ):


            cleaning_result = (

                execute_step(

                    state,

                    "cleaning",

                    run_cleaning_step,

                    monitor,

                    dataframe,

                    understanding_result,

                    quality_result,

                    True
                )
            )


            results[
                "cleaning"
            ] = cleaning_result


            # Get cleaned dataframe safely

            if isinstance(
                cleaning_result,
                dict
            ):

                cleaned_dataframe = (

                    cleaning_result.get(
                        "dataframe",
                        cleaning_result.get(
                            "cleaned_dataframe",
                            dataframe
                        )
                    )
                )

            else:

                cleaned_dataframe = (
                    cleaning_result
                )


        # =================================================
        # ANALYSIS
        # =================================================

        analysis_result = None


        if pipeline_config.get(
            "run_analysis",
            True
        ):


            analysis_result = (

                execute_step(

                    state,

                    "analysis",

                    run_analysis_step,

                    monitor,

                    cleaned_dataframe,

                    understanding_result
                )
            )


            results[
                "analysis"
            ] = analysis_result


        # =================================================
        # ANOMALY DETECTION
        # =================================================

        anomaly_result = None


        if pipeline_config.get(
            "run_anomaly_detection",
            True
        ):


            anomaly_result = (

                execute_step(

                    state,

                    "anomaly_detection",

                    run_anomaly_step,

                    monitor,

                    cleaned_dataframe
                )
            )


            results[
                "anomaly"
            ] = anomaly_result


        # =================================================
        # INTELLIGENCE
        # =================================================

        intelligence_result = None


        if pipeline_config.get(
            "run_intelligence",
            True
        ):


            intelligence_result = (

                execute_step(

                    state,

                    "intelligence",

                    run_intelligence_step,

                    monitor,

                    cleaned_dataframe,

                    results
                )
            )


            results[
                "intelligence"
            ] = intelligence_result


        # =================================================
        # VISUALIZATION
        # =================================================

        if pipeline_config.get(
            "run_visualization",
            True
        ):


            results[
                "visualization"
            ] = execute_step(

                state,

                "visualization",

                run_visualization_step,

                monitor,

                cleaned_dataframe,

                project_id
            )


        # =================================================
        # MACHINE LEARNING RECOMMENDATIONS
        # =================================================

        ml_recommendations = None


        if pipeline_config.get(
            "run_machine_learning",
            True
        ):


            ml_recommendations = (

                execute_step(

                    state,

                    "ml_recommendations",

                    run_ml_recommendation_step,

                    monitor,

                    cleaned_dataframe
                )
            )


            results[
                "ml_recommendations"
            ] = ml_recommendations


        # =================================================
        # REPORTING
        # =================================================

        final_report = None


        if pipeline_config.get(
            "run_reporting",
            True
        ):


            final_report = (

                execute_step(

                    state,

                    "reporting",

                    run_reporting_step,

                    monitor,

                    cleaned_dataframe,

                    understanding_result,

                    profiling_result,

                    quality_result,

                    cleaning_result,

                    analysis_result,

                    anomaly_result,

                    ml_recommendations,

                    None
                )
            )


            results[
                "final_report"
            ] = final_report


        # =================================================
        # STORAGE
        # =================================================

        if pipeline_config.get(
            "run_storage",
            True
        ):


            results[
                "storage"
            ] = execute_step(

                state,

                "storage",

                save_project_results,

                monitor,

                project_id=project_id,

                original_dataframe=original_dataframe,

                cleaned_dataframe=cleaned_dataframe,

                final_report=final_report,

                intelligence_result=intelligence_result
            )


        # =================================================
        # COMPLETE PIPELINE
        # =================================================

        state.complete_pipeline()


        # =================================================
        # STOP MONITORING
        # =================================================

        if monitor is not None:


            monitor.stop_pipeline()


            results[
                "monitoring"
            ] = (

                monitor.get_pipeline_report()
            )


        # =================================================
        # PIPELINE STATE
        # =================================================

        results[
            "pipeline_state"
        ] = state.to_dict()


        results[
            "from_cache"
        ] = False


        # =================================================
        # SAVE CACHE
        # =================================================

        if pipeline_config.get(
            "run_cache",
            True
        ):


            save_cached_result(

                file_path,

                results
            )


        # =================================================
        # LOG SUCCESS
        # =================================================

        log_pipeline_complete()


        return results


    # =====================================================
    # PIPELINE FAILURE
    # =====================================================

    except Exception as error:


        state.fail_pipeline()


        if monitor is not None:


            monitor.stop_pipeline()


            results[
                "monitoring"
            ] = (

                monitor.get_pipeline_report()
            )


        results[
            "pipeline_state"
        ] = state.to_dict()


        results[
            "error"
        ] = str(error)


        log_pipeline_failed(
            error
        )


        return results

