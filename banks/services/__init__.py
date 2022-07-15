from ..constants import DataExportType
from .base import BaseGenerateReportService
from .csv_report import GenerateCSVReportService


def report_service_proxy(data_type: str) -> BaseGenerateReportService:
    if data_type == DataExportType.CSV:
        return GenerateCSVReportService()
