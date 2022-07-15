from django.shortcuts import render
from django.http.response import Http404
from .services import report_service_proxy
from .constants import DataExportType


def create_report_view(request):
    if request.method == "POST":
        data_type: str = request.POST.get("data_type")
        if data_type not in DataExportType.values:
            raise Http404(f"Presented data type {data_type} is not available.")
        report_service = report_service_proxy(data_type)
        return report_service.generate_response()

    context: dict = {"data_types": DataExportType.choices}
    return render(request, "banks/report.html", context)
