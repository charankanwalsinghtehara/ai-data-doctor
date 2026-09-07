from django.db import models


class Dataset(models.Model):
    name = models.CharField(
        max_length=255
    )

    file = models.FileField(
        upload_to="datasets/"
    )

    file_size = models.PositiveBigIntegerField(
        default=0
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class AnalysisHistory(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="analyses"
    )

    analysis_result = models.JSONField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Analysis {self.id} - {self.dataset.name}"

class MLModelHistory(models.Model):

    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name="ml_models"
    )

    target_column = models.CharField(
        max_length=255
    )

    problem_type = models.CharField(
        max_length=50
    )

    best_model = models.CharField(
        max_length=255
    )

    model_results = models.JSONField()

    feature_importance = models.JSONField(
        default=list
    )

    model_file = models.CharField(
        max_length=500
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.dataset.name} - "
            f"{self.best_model}"
        )