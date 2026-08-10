import io
from pathlib import Path

import streamlit as st
from docx_utils import read_docx, get_text, write_docx, replace_placeholder, find_placeholders

DEFAULT_TEMPLATE_PATH = Path(__file__).parent / "lease_template.docx"

st.set_page_config(layout="wide")

st.title("Simple Lease Generator")
st.subheader("[Full documentation](https://github.com/wcah/simple_lease_generator)")

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
                values[placeholder] = st.text_input(
                    f"{placeholder}", value=f"{placeholder}", key=f"placeholder_{placeholder}"
                )

        for placeholder, value in values.items():
            replace_placeholder(doc, placeholder, value)
    else:
        st.info("No [[PLACEHOLDER]] tokens were found in this document.")

with right:
    st.subheader("Document Preview")
    preview_html = get_text(doc).replace("\n", "<br>")
    st.markdown(
        f'<div style="height: 600px; overflow-y: auto; border: 1px solid #ddd; padding: 1rem; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap;">{preview_html}</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Download")
    buffer = io.BytesIO()
    write_docx(doc, buffer)
    buffer.seek(0)
    st.download_button(
        label="Fill All & Download",
        data=buffer,
        file_name="filled_output.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
