import json
import pandas as pd

from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class JSONExtractor(BaseExtractor):

    def extract(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                json_data = json.load(file)

            if isinstance(json_data, list):

                dataframe = pd.json_normalize(
                    json_data
                )

                data = dataframe
                data_kind = "dataframe"

            elif isinstance(json_data, dict):

                dataframe = pd.json_normalize(
                    json_data
                )

                data = dataframe
                data_kind = "dataframe"

            else:

                data = json_data
                data_kind = "raw_json"

            metadata = {
                "data_kind": data_kind
            }

            if isinstance(data, pd.DataFrame):

                metadata.update({
                    "rows": int(data.shape[0]),
                    "columns": int(data.shape[1]),
                    "column_names": data.columns.tolist()
                })

            return {
                "data": data,
                "metadata": metadata
            }

        except Exception as error:

            raise FileExtractionError(
                f"Failed to extract JSON file: {error}"
            )