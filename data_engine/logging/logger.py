import logging

from ...app_config.paths import (
    LOGS_DIR
)


def get_logger(
    name="ai_data_doctor"
):
    """
    Create and return
    application logger.
    """

    LOGS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(
        name
    )

    logger.setLevel(
        logging.DEBUG
    )

    # Prevent duplicate handlers

    if logger.handlers:

        return logger


    # =========================
    # FILE HANDLER
    # =========================

    log_file = (
        LOGS_DIR
        / "ai_data_doctor.log"
    )

    file_handler = (
        logging.FileHandler(
            log_file,
            encoding="utf-8"
        )
    )

    file_handler.setLevel(
        logging.DEBUG
    )


    # =========================
    # CONSOLE HANDLER
    # =========================

    console_handler = (
        logging.StreamHandler()
    )

    console_handler.setLevel(
        logging.INFO
    )


    # =========================
    # FORMAT
    # =========================

    formatter = logging.Formatter(

        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )


    file_handler.setFormatter(
        formatter
    )

    console_handler.setFormatter(
        formatter
    )


    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )


    return logger