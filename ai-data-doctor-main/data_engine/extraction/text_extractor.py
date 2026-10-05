from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class TextExtractor(BaseExtractor):

    def extract(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

            return {
                "data": text,

                "metadata": {
                    "data_kind": "text",
                    "characters": len(text),
                    "lines": len(text.splitlines())
                }
            }

        except UnicodeDecodeError:

            try:

                with open(
                    file_path,
                    "r",
                    encoding="latin-1"
                ) as file:

                    text = file.read()

                return {
                    "data": text,

                    "metadata": {
                        "data_kind": "text",
                        "characters": len(text),
                        "lines": len(text.splitlines()),
                        "encoding": "latin-1"
                    }
                }

            except Exception as error:

                raise FileExtractionError(
                    f"Failed to extract text file: {error}"
                )

        except Exception as error:

            raise FileExtractionError(
                f"Failed to extract text file: {error}"
            )