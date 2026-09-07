def create_pipeline_config(
    custom_config=None
):
    """
    Create the default configuration
    for the AI Data Doctor pipeline.
    """

    default_config = {

        # =========================
        # CACHE
        # =========================

        "run_cache": True,


        # =========================
        # VALIDATION
        # =========================

        "run_validation": True,


        # =========================
        # DATA LOADING
        # =========================

        "run_ingestion": True,

        "run_extraction": True,


        # =========================
        # METADATA
        # =========================

        "run_metadata": True,


        # =========================
        # DATA UNDERSTANDING
        # =========================

        "run_understanding": True,

        "run_profiling": True,

        "run_quality": True,


        # =========================
        # DATA PROCESSING
        # =========================

        "run_cleaning": True,

        "run_preprocessing": True,


        # =========================
        # DATA ANALYSIS
        # =========================

        "run_analysis": True,

        "run_anomaly_detection": True,


        # =========================
        # MACHINE LEARNING
        # =========================

        "run_machine_learning": True,


        # =========================
        # INTELLIGENCE
        # =========================

        "run_intelligence": True,


        # =========================
        # OUTPUT
        # =========================

        "run_reporting": True,

        "run_visualization": True,


        # =========================
        # STORAGE
        # =========================

        "run_storage": True,

        "run_export": False,


        # =========================
        # MONITORING
        # =========================

        "run_monitoring": True
    }


    # =========================
    # CUSTOM CONFIGURATION
    # =========================

    if custom_config:

        default_config.update(
            custom_config
        )


    return default_config