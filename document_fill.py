from docx_utils import read_docx, write_docx, replace_placeholder


def fill_document(docx_path: str, replacements: dict[str, str], output_path: str) -> None:
    doc = read_docx(docx_path)
    for placeholder, value in replacements.items():
        replace_placeholder(doc, placeholder, value)
    write_docx(doc, output_path, source_path=docx_path)
