from .csv_extractor import CSVExtractor
from .excel_extractor import ExcelExtractor
from .json_extractor import JSONExtractor
from .parquet_extractor import ParquetExtractor
from .xml_extractor import XMLExtractor
from .text_extractor import TextExtractor
from .pdf_extractor import PDFExtractor
from .docx_extractor import DOCXExtractor
from .image_extractor import ImageExtractor

from .exceptions import ExtractorNotFoundError


EXTRACTORS = {

    "csv": CSVExtractor(),

    "excel": ExcelExtractor(),

    "json": JSONExtractor(),

    "parquet": ParquetExtractor(),

    "xml": XMLExtractor(),

    "text": TextExtractor(),

    "pdf": PDFExtractor(),

    "docx": DOCXExtractor(),

    "image": ImageExtractor()
}


def get_extractor(file_type):
    """
    Return the correct extractor object.
    """

    extractor = EXTRACTORS.get(file_type)

    if extractor is None:

        raise ExtractorNotFoundError(
            f"No extractor found for file type: "
            f"{file_type}"
        )

    return extractor


def extract_file(file_path, file_type):
    """
    Extract data using the correct extractor.
    """

    extractor = get_extractor(file_type)

    return extractor.extract(file_path)