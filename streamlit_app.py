import streamlit as st

# from view.main_panel import set_main_view
from view.study_content import set_main_view
# from view.student_identification import set_identification_form
from view.study_selection import select_study_view

# Set browser tab name and potential
st.set_page_config("Learning app", layout="wide")

# st.write("-----------")

select_study_view()

# st.write("-----------")

if "study_path" in st.session_state.keys():
    set_main_view()
