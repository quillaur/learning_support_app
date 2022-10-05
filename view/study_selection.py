import streamlit as st
from os import listdir
from os.path import join, isdir


def select_study_view():
    """
    This function defines the layout of the page to select a study in the app.
    """
    
    st.sidebar.title("Select your Study")
    
    selected_language = st.sidebar.selectbox("Language:", [d for d in listdir("classes/") if isdir(join("classes/", d))])
    language_path = join("classes", selected_language)
    selected_category = st.sidebar.selectbox("Category:", [d for d in listdir(language_path) if isdir(join(language_path, d))])
    category_path = join(language_path, selected_category)
    selected_study = st.sidebar.selectbox("Study:", [d for d in listdir(category_path) if isdir(join(category_path, d))])
    select = st.sidebar.button("Select")

    if select:
        st.session_state["selected_study"] = selected_study
        st.session_state["study_path"] = join(category_path, selected_study)
        st.session_state["score"] = 0

    