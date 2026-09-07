from django.contrib import admin

from .models import (
Dataset,
AnalysisHistory
)

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):


     list_display = (

    "id",

    "name",

    "file_size",

    "uploaded_at",

)


@admin.register(AnalysisHistory)
class AnalysisHistoryAdmin(admin.ModelAdmin):


    list_display = (

    "id",

    "dataset",

    "created_at",

)

