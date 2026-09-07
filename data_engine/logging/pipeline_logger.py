from .logger import (
    get_logger
)


logger = get_logger(
    "pipeline"
)


def log_pipeline_start(
    project_name=None
):
    """
    Log pipeline start.
    """

    logger.info(
        "AI Data Doctor pipeline started."
    )

    if project_name:

        logger.info(

            f"Project: "
            f"{project_name}"
        )


def log_step_start(
    step_name
):
    """
    Log pipeline step start.
    """

    logger.info(

        f"Starting step: "
        f"{step_name}"
    )


def log_step_complete(
    step_name
):
    """
    Log successful step completion.
    """

    logger.info(

        f"Completed step: "
        f"{step_name}"
    )


def log_step_failed(
    step_name,
    error
):
    """
    Log failed pipeline step.
    """

    logger.error(

        f"Failed step: "
        f"{step_name} | "
        f"Error: {error}"
    )


def log_pipeline_complete():
    """
    Log successful pipeline completion.
    """

    logger.info(
        "AI Data Doctor pipeline completed successfully."
    )


def log_pipeline_failed(
    error
):
    """
    Log pipeline failure.
    """

    logger.exception(

        f"Pipeline failed: "
        f"{error}"
    )