import streamlit as st
def render_sidebar(conversations):
    with st.sidebar:
        st.title("Enterprise AI"); st.caption("Memory + knowledge retrieval")
        user = st.text_input("User identity", value=st.session_state.get("external_id", "demo-user"))
        new = st.button("＋ New chat", use_container_width=True); st.divider(); st.subheader("Conversations")
        selected = None
        for c in conversations:
            if st.button(c.title, key=f"c{c.id}", use_container_width=True): selected = c.id
        return user, new, selected

