import streamlit as st
def render_documents(upload_callback):
    with st.expander("Knowledge base"):
        upload = st.file_uploader("Upload PDF, TXT, DOCX, or Markdown", type=["pdf", "txt", "docx", "md"])
        if upload and st.button("Index document"):
            try: st.success(upload_callback(upload)[1])
            except Exception as exc: st.error(str(exc))

