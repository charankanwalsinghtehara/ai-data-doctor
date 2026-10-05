import pandas as pd

from .extractor_manager import extract_file
from .exceptions import FileExtractionError


def extract_data(file_path, file_info):
    """Main extraction pipeline with normalized extractor output."""
    file_type = file_info["file_type"]

    extraction_result = extract_file(
        file_path=file_path,
        file_type=file_type,
    )

    # All project extractors should return {"data": ..., "metadata": ...}.
    # Normalize a direct DataFrame return as a safety fallback.
    if isinstance(extraction_result, pd.DataFrame):
        extraction_result = {
            "data": extraction_result,
            "metadata": {
                "data_kind": "dataframe",
                "rows": int(extraction_result.shape[0]),
                "columns": int(extraction_result.shape[1]),
                "column_names": extraction_result.columns.astype(str).tolist(),
            },
        }

    if not isinstance(extraction_result, dict):
        raise FileExtractionError(
            f"Extractor returned unsupported result type: {type(extraction_result).__name__}"
        )

    if "data" not in extraction_result:
        raise FileExtractionError(
            "Extractor returned no 'data' key. "
            f"Available keys: {list(extraction_result.keys())}"
        )

    return {
        "success": True,
        "file_type": file_type,
        "data": extraction_result["data"],
        "metadata": extraction_result.get("metadata", {}),
    }
