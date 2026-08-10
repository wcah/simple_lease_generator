import io
from pathlib import Path

import streamlit as st
from st_keyup import st_keyup

from docx_utils import read_docx, get_text, write_docx, replace_placeholder, find_placeholders

DEFAULT_TEMPLATE_PATH = Path(__file__).parent / "lease_template.docx"

st.set_page_config(layout="wide")

st.title("Simple Lease Generator - [full documentation](https://github.com/wcah/simple_lease_generator)")

docx_file = st.file_uploader(
    "Upload a .docx template (optional — defaults to the built-in lease template)",
    type=["docx"],
)

if docx_file:
    doc = read_docx(io.BytesIO(docx_file.read()))
else:
    doc = read_docx(str(DEFAULT_TEMPLATE_PATH))
    st.caption(f"No template uploaded — using the default: {DEFAULT_TEMPLATE_PATH.name}")

left, right = st.columns([1, 1])

with left:
    title_col, download_col = st.columns([3, 1])
    with title_col:
        st.subheader(
            "Fill Placeholders",
            help=(
                "Each box is pre-filled with its placeholder token; "
                "edit the ones you want to replace and leave the rest as-is."
            ),
        )

    placeholders = find_placeholders(doc)

    if placeholders:
        values = {}
        col_a, col_b = st.columns(2)
        for i, placeholder in enumerate(placeholders):
            with col_a if i % 2 == 0 else col_b:
                values[placeholder] = st_keyup(
                    f"{placeholder}",
                    placeholder=f"{placeholder}",
                    key=f"placeholder_{placeholder}",
                    debounce=250,
                )

        for placeholder, value in values.items():
            replace_placeholder(doc, placeholder, value or "")
    else:
        st.info("No [[PLACEHOLDER]] tokens were found in this document.")

    buffer = io.BytesIO()
    write_docx(doc, buffer)
    buffer.seek(0)
    with download_col:
        st.download_button(
            label="Fill All & Download",
            data=buffer,
            file_name="filled_output.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

with right:
    st.subheader("Document Preview")
    preview_html = get_text(doc).replace("\n", "<br>")
    st.markdown(
        f'<div style="height: calc(100vh - 420px); min-height: min(100px, 15vh); overflow-y: auto; border: 1px solid #ddd; padding: 1rem; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap;">{preview_html}</div>',
        unsafe_allow_html=True,
    )
