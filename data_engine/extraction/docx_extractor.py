from docx import Document

from .base_extractor import BaseExtractor
from .exceptions import FileExtractionError


class DOCXExtractor(BaseExtractor):

    def extract(self, file_path):

        try:

            document = Document(file_path)

            paragraphs = []

            for paragraph in document.paragraphs:

                text = paragraph.text.strip()

                if text:

                    paragraphs.append(text)

            full_text = "\n".join(paragraphs)

            return {
                "data": full_text,

                "metadata": {
                    "data_kind": "text",
                    "paragraph_count": len(paragraphs),
                    "characters": len(full_text)
                }
            }

        except Exception as error:

            raise FileExtractionError(
                f"Failed to extract DOCX file: {error}"
            )