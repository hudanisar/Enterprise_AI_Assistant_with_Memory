import streamlit as st
def render_memories(memories):
    with st.expander("🧠 Your memories"):
        for m in memories: st.caption(f"{m.memory_type.title()}: {m.content}")
        if not memories: st.caption("No persistent memories yet.")

