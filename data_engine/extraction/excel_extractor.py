import pandas as pd

from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class ExcelExtractor(BaseExtractor):

    def extract(self, file_path):

        try:

            excel_file = pd.ExcelFile(file_path)

            sheets = {}

            for sheet_name in excel_file.sheet_names:

                dataframe = pd.read_excel(
                    file_path,
                    sheet_name=sheet_name
                )

                sheets[sheet_name] = dataframe

            return {
                "data": sheets,

                "metadata": {
                    "data_kind": "multiple_dataframes",
                    "sheet_count": len(sheets),
                    "sheet_names": list(sheets.keys())
                }
            }

        except Exception as error:

            raise FileExtractionError(
                f"Failed to extract Excel file: {error}"
            )