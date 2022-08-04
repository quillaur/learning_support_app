import streamlit as st

def set_identification_form(title_holder: st.empty, main_holder: st.empty, available_classes: list) -> None:
    title_holder.title("Identification form")
    with main_holder.form("Identification"):
        firstname = st.text_input("Firstname:")
        lastname = st.text_input("Lastname:")
        your_class = st.text_input("Your class:")
        selected_study = st.selectbox("Please select what you would like to study:", available_classes)

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["firstname"] = firstname
            st.session_state["lastname"] = lastname
            st.session_state["class"] = your_class
            st.session_state["selected_study"] = selected_study
            st.session_state["support_number"] = 0