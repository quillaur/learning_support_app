import streamlit as st
from os import listdir
from os.path import join, isdir


def select_study_view():
    """
    This function defines the layout of the page to select a study in the app.
    """
    # center title
    _, col2, _ = st.columns(3)
    with col2:
        st.title("Select your Study")

    # What studies are available ?
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        # Show a welcomy image
        # st.image("view/love_to_learn_and_teach.jpg")
        # Filter by language first.    
        selected_language = st.selectbox("Language:", [d for d in listdir("classes/") if isdir(join("classes/", d))])
        language_path = join("classes", selected_language)
        
    with col2:            
        # Then filter by category.
        selected_category = st.selectbox("Category:", [d for d in listdir(language_path) if isdir(join(language_path, d))])
        category_path = join(language_path, selected_category)
    
    with col3:
        # After applying filters, show which study can be selected.
        selected_study = st.selectbox("Study:", [d for d in listdir(category_path) if isdir(join(category_path, d))])
        # The select button determine when to save the results in the session state object.
    
    select = st.button("Select")

    if select:
        st.session_state["selected_study"] = selected_study
        st.session_state["study_path"] = join(category_path, selected_study)
        st.session_state["score"] = 0

    