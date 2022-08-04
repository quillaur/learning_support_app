import streamlit as st

def set_side_panel_view() -> None:
    st.sidebar.write(f"Firstname : {st.session_state['firstname']}")
    st.sidebar.write(f"lastname : {st.session_state['lastname']}")
    st.sidebar.write(f"Class : {st.session_state['class']}")
    st.sidebar.write(f"Selected study : {st.session_state['selected_study']}")
    st.sidebar.write(f"Page: {st.session_state['support_number']}")