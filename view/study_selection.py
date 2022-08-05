import streamlit as st
from os import listdir
from os.path import join


def select_study_view(main_holder: st.empty):

    with main_holder.container():
        st.title("What do you want to study ?")

        # What studies are available ?
        col1, col2 = st.columns(2)
        with col1:
            selected_language = st.selectbox("Language:", listdir("classes/"))
            language_path = join("classes", selected_language)
        with col2:
            selected_category = st.selectbox("Category:", listdir(language_path))
            category_path = join(language_path, selected_category)

        selected_study = st.selectbox("Please select what you would like to study:", listdir(category_path))
        
        select = st.button("Select")
    
    if select:
        st.session_state["selected_study"] = selected_study
        st.session_state["study_path"] = join(category_path, selected_study)
        st.session_state["support_number"] = 0

        main_holder.empty()

    