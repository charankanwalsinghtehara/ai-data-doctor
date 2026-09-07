from rest_framework import serializers

from .models import Dataset, AnalysisHistory
from .models import (
    Dataset,
    AnalysisHistory,
    MLModelHistory
)
class DatasetSerializer(serializers.ModelSerializer):

    class Meta:

        model = Dataset

        fields = [

            "id",

            "name",

            "file",

            "file_size",

            "uploaded_at",

        ]

        read_only_fields = [

            "file_size",

            "uploaded_at",

        ]


def validate_file(self, value):

    allowed_extensions = [

        ".csv",

        ".xlsx",

        ".xls",

    ]

    file_name = value.name.lower()


    if not any(
        file_name.endswith(extension)
        for extension in allowed_extensions
    ):

        raise serializers.ValidationError(

            "Only CSV, XLSX, and XLS files are supported."

        )


    # Maximum file size: 50 MB
    max_size = 50 * 1024 * 1024


    if value.size > max_size:

        raise serializers.ValidationError(

            "Maximum allowed file size is 50 MB."

        )


    return value


class AnalysisHistorySerializer(serializers.ModelSerializer):

    class Meta:

        model = AnalysisHistory

        fields = [

            "id",

            "dataset",

            "analysis_result",

            "created_at",

        ]

        read_only_fields = [

            "created_at",

        ]

class MLModelHistorySerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = MLModelHistory

        fields = "__all__"