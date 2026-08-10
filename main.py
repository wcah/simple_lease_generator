import io
import streamlit as st
from docx_utils import read_docx, get_text, write_docx, replace_placeholder
from xlsx_utils import read_xlsx_to_dict

st.title("DOCX Form Filler")
st.subheader("For full documentation:\nhttps://github.com/wcah/docx_template_filler")

docx_file = st.file_uploader("Upload a .docx template", type=["docx"])

if docx_file:
    doc = read_docx(io.BytesIO(docx_file.read()))

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Fill Placeholders")

        method = st.radio("Replacement method", ["Manual", "Upload .xlsx"])

        if method == "Manual":
            placeholder = st.text_input("Placeholder name (without $)")
            replacement = st.text_input("Replace with")

            if st.button("Replace") and placeholder:
                replace_placeholder(doc, placeholder, replacement)
                st.success(f"Replaced ${placeholder.upper()} with '{replacement}'")

        else:
            xlsx_file = st.file_uploader("Upload .xlsx (column 1 = placeholders, column 2 = values)", type=["xlsx"])

            if xlsx_file:
                replacements = read_xlsx_to_dict(io.BytesIO(xlsx_file.read()))
                st.write("Replacements found:", replacements)

                if st.button("Fill All"):
                    for placeholder, value in replacements.items():
                        replace_placeholder(doc, placeholder, value)
                    st.success("All placeholders replaced.")

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
