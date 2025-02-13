import streamlit as st

if "name" not in st.session_state:
    st.session_state["name"] = "My counter name"

if "counter" not in st.session_state:
    st.session_state["counter"] = 0

st.write(
    f"The counter for '{st.session_state["name"]}' is currently {st.session_state["counter"]}"
)

st.text_input(label="Counter name", key="name")

if st.button(label=f"Increase '{st.session_state["name"]}'"):
    st.session_state["counter"] += 1
