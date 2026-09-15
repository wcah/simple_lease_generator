import io
import re

from docx import Document as Doc
from docx.document import Document

PLACEHOLDER_PATTERN = re.compile(r"\[\[([A-Za-z][A-Za-z0-9_]*)\]\]")


def read_docx(source: str | io.BytesIO) -> Document:
    return Doc(source)


def get_text(doc: Document) -> str:
    return "\n".join(para.text for para in doc.paragraphs)


def find_placeholders(doc: Document) -> list[str]:
    found = set()
    for para in doc.paragraphs:
        found.update(match.upper() for match in PLACEHOLDER_PATTERN.findall(para.text))
    return sorted(found)


def write_docx(doc: Document, target: str | io.BytesIO, source_path: str | None = None) -> None:
    if source_path and isinstance(target, str) and target == source_path:
        raise ValueError(f"Refusing to overwrite source file: {source_path}")
    doc.save(target)


def replace_placeholder(doc: Document, placeholder: str, replacement: str) -> None:
    token = f"[[{placeholder.upper()}]]"
    for para in doc.paragraphs:
        _replace_in_paragraph(para, token, replacement)


def _replace_in_paragraph(paragraph, token: str, replacement: str) -> None:
    # A token can be split across multiple runs (e.g. by spell-check markers or
    # formatting boundaries), so `token in run.text` alone misses those
    # occurrences. Locate the token in the paragraph's full text instead, map
    # that span back onto the runs it crosses, and merge them.
    while token in paragraph.text:
        runs = paragraph.runs
        texts = [run.text for run in runs]
        full_text = "".join(texts)
        start = full_text.find(token)
        end = start + len(token)

        offset = 0
        start_run = end_run = None
        start_offset = end_offset = 0
        for i, text in enumerate(texts):
            run_start, run_end = offset, offset + len(text)
            if start_run is None and run_start <= start < run_end:
                start_run = i
                start_offset = start - run_start
            if run_start < end <= run_end:
                end_run = i
                end_offset = end - run_start
                break
            offset = run_end

        if start_run is None or end_run is None:
            break

        if start_run == end_run:
            run = runs[start_run]
            run.text = run.text[:start_offset] + replacement + run.text[end_offset:]
        else:
            runs[start_run].text = texts[start_run][:start_offset] + replacement
            for i in range(start_run + 1, end_run):
                runs[i].text = ""
            runs[end_run].text = texts[end_run][end_offset:]



