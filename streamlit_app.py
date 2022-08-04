import streamlit as st
from control.content import load_study_content
from view.main_panel import set_main_view
from view.side_panel import set_side_panel_view
from view.student_identification import set_identification_form
from view.study_selection import select_study_view

# To change content from one page to another, 
# I need to initialize empty containers and clear / fill them as needed.
main_holder = st.empty()

##########################
# Student identification #
##########################
if "firstname" not in st.session_state:
    set_identification_form(main_holder)

if "firstname" in st.session_state:
    ########################
    # Study selection page #
    ########################
    select_study_view(main_holder)

# How many supports ?
if "support_number" in st.session_state:
    load_study_content()

    ##############
    # Side Panel #
    ##############
    set_side_panel_view()

    #############
    # Main Page #
    #############
    set_main_view(main_holder)
