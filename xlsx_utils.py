import io

import openpyxl


def read_xlsx_to_dict(source: str | io.BytesIO, sheet_name: str | None = None) -> dict[str, str]:
    wb = openpyxl.load_workbook(source, read_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active
    result = {}
    for row in ws.iter_rows(min_row=2, max_col=2, values_only=True):
        key, value = row
        if key is not None:
            result[str(key)] = str(value) if value is not None else ""
    wb.close()
    return result



