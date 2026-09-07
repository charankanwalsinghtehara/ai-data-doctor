import pandas as pd

from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class XMLExtractor(BaseExtractor):

    def extract(self, file_path):

        try:

            dataframe = pd.read_xml(
                file_path
            )

            return {
                "data": dataframe,

                "metadata": {
                    "data_kind": "dataframe",
                    "rows": int(dataframe.shape[0]),
                    "columns": int(dataframe.shape[1]),
                    "column_names": dataframe.columns.tolist()
                }
            }

        except Exception as error:

            raise FileExtractionError(
                f"Failed to extract XML file: {error}"
            )