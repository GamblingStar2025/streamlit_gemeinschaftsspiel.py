import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.switch_page("login.py")
else:
    st.title("🎉 Willkommen in deinem Dashboard!")
    st.write(f"Eingeloggt als: {st.session_state.get('email')}")