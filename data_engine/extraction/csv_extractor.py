import csv
from pathlib import Path

import pandas as pd

from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class CSVExtractor(BaseExtractor):
    """Robust CSV extractor that tolerates encoding and malformed-row issues."""

    def extract(self, file_path):
        file_path = Path(file_path)
        last_error = None

        attempts = [
            {"encoding": "utf-8", "engine": "c"},
            {"encoding": "utf-8-sig", "engine": "c"},
            {"encoding": "latin-1", "engine": "c"},
            {"encoding": "utf-8", "engine": "python", "on_bad_lines": "skip"},
            {"encoding": "latin-1", "engine": "python", "on_bad_lines": "skip"},
        ]

        for options in attempts:
            try:
                dataframe = pd.read_csv(file_path, **options)
                return {
                    "data": dataframe,
                    "metadata": {
                        "data_kind": "dataframe",
                        "rows": int(dataframe.shape[0]),
                        "columns": int(dataframe.shape[1]),
                        "column_names": dataframe.columns.astype(str).tolist(),
                    },
                }
            except Exception as error:
                last_error = error

        raise FileExtractionError(
            f"Failed to extract CSV file '{file_path.name}': {last_error}"
        )
