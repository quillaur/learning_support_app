import streamlit as st
from os import listdir
from os.path import join


def select_study_view(main_holder: st.empty):

    with main_holder.container():
        st.title("What do you want to study ?")

        # What studies are available ?
        col1, col2 = st.columns(2)
        with col1:
            selected_category = st.selectbox("Filter by category:", listdir("classes/"))
            category_path = join("classes", selected_category)
        with col2:
            selected_study = st.selectbox("Please select what you would like to study:", listdir(category_path))
        
        select = st.button("Select")
    
    if select:
        st.session_state["selected_study"] = selected_study
        st.session_state["study_path"] = join("classes", selected_category, selected_study)
        st.session_state["support_number"] = 0


    