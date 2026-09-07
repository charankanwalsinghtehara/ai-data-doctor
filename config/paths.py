from pathlib import Path


# Root project directory

BASE_DIR = (

    Path(__file__)

    .resolve()

    .parent

    .parent
)


# =========================
# MAIN DIRECTORIES
# =========================

DATA_ENGINE_DIR = (

    BASE_DIR

    / "data_engine"
)


STORAGE_DIR = (

    BASE_DIR

    / "storage"
)


DATASETS_DIR = (

    BASE_DIR

    / "datasets"
)


EXPORTS_DIR = (

    BASE_DIR

    / "exports"
)


LOGS_DIR = (

    BASE_DIR

    / "logs"
)


# =========================
# CREATE DIRECTORIES
# =========================

DIRECTORIES = [

    STORAGE_DIR,

    DATASETS_DIR,

    EXPORTS_DIR,

    LOGS_DIR
]


def create_project_directories():

    for directory in DIRECTORIES:

        directory.mkdir(

            parents=True,

            exist_ok=True
        )


def get_project_root():

    return BASE_DIR