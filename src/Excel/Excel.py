from openpyxl import Workbook

class Excel:

    def __init__(self, headers, data):
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.number_line_appended = 0

        self.appendHeaders(headers)

    def appendHeaders(self, headers):
        for col_num, valeur in enumerate(headers, start=1):
            self.sheet.cell(row=1, column=col_num, value=valeur)

    def appendData(self, data):
        for infos in data:
            self.sheet.append(infos)
            self.number_line_appended += 1

    def save(self, filename):
        self.workbook.save(f"excel/{filename}")