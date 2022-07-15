from django.db.models import TextChoices


class DataExportType(TextChoices):
    CSV = "csv"
