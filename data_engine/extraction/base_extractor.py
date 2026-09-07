from abc import ABC, abstractmethod


class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, file_path):
        """
        Extract data from a file.

        Every extractor must return a dictionary
        containing data and metadata.
        """

        pass