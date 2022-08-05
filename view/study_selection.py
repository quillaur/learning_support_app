import json
import streamlit as st
from os import listdir
from os.path import join


def select_study_view(main_holder: st.empty):

    with main_holder.container():
        st.title("What do you want to study ?")

        # What studies are available ?
        col1, col2 = st.columns(2)
        with col1:
            selected_language = st.selectbox("Language:", ["English", "Français"])
        with col2:
            selected_category = st.selectbox("Category:", listdir("classes/"))
            category_path = join("classes", selected_category)

        filtered_studies = []
        for s in listdir(category_path):
            config_path = join(category_path, s, "config.json")
            with open(config_path, "r") as json_file:
                json_content = json.load(json_file)
            
            if json_content["language"] == selected_language:
                filtered_studies.append(s)

        selected_study = st.selectbox("Please select what you would like to study:", filtered_studies)
        
        select = st.button("Select")
    
    if select:
        st.session_state["selected_study"] = selected_study
        st.session_state["study_path"] = join("classes", selected_category, selected_study)
        st.session_state["support_number"] = 0

        main_holder.empty()

    