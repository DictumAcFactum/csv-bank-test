from django.urls import path

from .views import create_report_view

urlpatterns = [
    path("report/", create_report_view),
]
