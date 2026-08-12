import streamlit as st
def render_chat(messages):
    for message in messages: st.chat_message(message.role).write(message.content)
def render_sources(sources):
    if sources:
        with st.expander("Sources"):
            for source in sources: st.markdown(f"📄 {source.get('filename','Document')} — page {source.get('page','n/a')}")

