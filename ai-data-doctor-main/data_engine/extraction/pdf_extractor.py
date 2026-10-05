from pypdf import PdfReader

from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class PDFExtractor(BaseExtractor):

    def extract(self, file_path):

        try:

            reader = PdfReader(file_path)

            pages = []

            for page_number, page in enumerate(
                reader.pages,
                start=1
            ):

                page_text = page.extract_text()

                pages.append({
                    "page": page_number,
                    "text": page_text or ""
                })

            full_text = "\n".join(
                page["text"]
                for page in pages
            )

            return {
                "data": full_text,

                "metadata": {
                    "data_kind": "text",
                    "page_count": len(reader.pages),
                    "characters": len(full_text),
                    "pages": pages
                }
            }

        except Exception as error:

            raise FileExtractionError(
                f"Failed to extract PDF file: {error}"
            )