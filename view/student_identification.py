import streamlit as st


def set_identification_form(main_holder: st.empty) -> None:

    with main_holder.form("ID form"):
        st.title("Identification form")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            firstname  = st.text_input("Firstname:")
        with col2:
            lastname = st.text_input("Lastname:")
        with col3:
            your_class = st.text_input("Your class:")

        if st.form_submit_button():
            st.session_state["firstname"] = firstname
            st.session_state["lastname"] = lastname
            st.session_state["class"] = your_class

            # For strange reasons, 
            # if I don't do a rerun after empty, 
            # not all elements are deleted...
            main_holder.empty()
            st.experimental_rerun()
   