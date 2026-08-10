from docx_utils import read_docx, write_docx, replace_placeholder
from xlsx_utils import read_xlsx_to_dict


def fill_document(docx_path: str, xlsx_path: str, output_path: str, sheet_name: str | None = None) -> None:
    doc = read_docx(docx_path)
    replacements = read_xlsx_to_dict(xlsx_path, sheet_name=sheet_name)
    for placeholder, value in replacements.items():
        replace_placeholder(doc, placeholder, value)
    write_docx(doc, output_path, source_path=docx_path)
