import io
import streamlit as st
from docx_utils import read_docx, get_text, write_docx, replace_placeholder, find_placeholders

st.title("DOCX Form Filler")
st.subheader("For full documentation:\nhttps://github.com/wcah/docx_template_filler")

docx_file = st.file_uploader("Upload a .docx template", type=["docx"])

if docx_file:
    doc = read_docx(io.BytesIO(docx_file.read()))

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Fill Placeholders")

        placeholders = find_placeholders(doc)

        if placeholders:
            st.caption(
                "Each box is pre-filled with its placeholder token; "
                "edit the ones you want to replace and leave the rest as-is."
            )
            values = {
                placeholder: st.text_input(
                    f"[[{placeholder}]]", value=f"[[{placeholder}]]", key=f"placeholder_{placeholder}"
                )
                for placeholder in placeholders
            }

            if st.button("Fill All"):
                for placeholder, value in values.items():
                    replace_placeholder(doc, placeholder, value)
                st.success("All placeholders replaced.")
        else:
            st.info("No [[PLACEHOLDER]] tokens were found in this document.")

        with st.expander("Replace a single placeholder manually"):
            placeholder = st.text_input("Placeholder name (e.g. LANDLORD_NAME)")
            replacement = st.text_input("Replace with")

            if st.button("Replace") and placeholder:
                replace_placeholder(doc, placeholder, replacement)
                st.success(f"Replaced [[{placeholder.upper()}]] with '{replacement}'")

        st.subheader("Download")
        buffer = io.BytesIO()
        write_docx(doc, buffer)
        buffer.seek(0)
        st.download_button(
            label="Download filled .docx",
            data=buffer,
            file_name="filled_output.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    with right:
        st.subheader("Document Preview")
        preview_html = get_text(doc).replace("\n", "<br>")
        st.markdown(
            f'<div style="height: 600px; overflow-y: auto; border: 1px solid #ddd; padding: 1rem; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap;">{preview_html}</div>',
            unsafe_allow_html=True,
        )
