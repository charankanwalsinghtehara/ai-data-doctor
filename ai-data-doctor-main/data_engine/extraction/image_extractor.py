from PIL import Image

from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class ImageExtractor(BaseExtractor):

    def extract(self, file_path):

        try:

            image = Image.open(file_path)

            metadata = {
                "data_kind": "image",

                "format": image.format,

                "width": image.width,

                "height": image.height,

                "mode": image.mode
            }

            return {
                "data": {
                    "image_path": str(file_path)
                },

                "metadata": metadata
            }

        except Exception as error:

            raise FileExtractionError(
                f"Failed to extract image: {error}"
            )