import os
import csv
from dateutil import parser
from django.http import HttpResponse

from .base import BaseGenerateReportService
from ..conf import CSV_DATA_FOLDER


class GenerateCSVReportService(BaseGenerateReportService):
    """ Generating CSV report """

    def generate_response(self) -> HttpResponse:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=bank_report.csv"
        writer = csv.writer(response)
        # headers
        writer.writerow(["date", "type", "amount", "to", "from"])

        csv_file_names: list = [f for f in os.listdir(CSV_DATA_FOLDER) if f.endswith(".csv")]
        csv_file_paths: list = [os.path.join(CSV_DATA_FOLDER, f) for f in csv_file_names]

        for file_path in csv_file_paths:
            for row in self.get_row_from_file(file_path):
                writer.writerow(row)
        return response

    def get_row_from_file(self, file_path: str) -> list:
        with open(file_path, mode="r") as csv_file:
            need_calculate_amount: bool = False
            csv_reader = csv.reader(csv_file)
            for i, row in enumerate(csv_reader):
                if i == 0:
                    if "euro" in row and "cents" in row:
                        need_calculate_amount = True
                    continue
                else:
                    yield self.row_to_representation(row, need_calculate_amount)

    def row_to_representation(self, row: list, need_calculate_amount: bool) -> list:
        row = self.calculate_amount(row) if need_calculate_amount else row
        row = self.convert_date(row)
        return row

    @staticmethod
    def calculate_amount(row: list) -> list:
        """ substitute 'euro' and 'cents' to 'amount' """
        euro, cents = row.pop(2), row.pop(2)
        amount = float(f"{euro}.{cents}")
        row.insert(2, amount)
        return row

    @staticmethod
    def convert_date(row) -> list:
        parsed_data = parser.parse(row[0])
        row[0] = parsed_data.strftime('%b %d %Y')
        return row
