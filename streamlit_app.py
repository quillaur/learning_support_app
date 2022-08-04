import json
import streamlit as st
from os.path import join
from os import listdir

from view.main_panel import set_main_view
from view.side_panel import set_side_panel_view
from view.student_identification import set_identification_form

# To change content from one page to another, 
# I need to initialize empty containers and clear / fill them as needed.
title_holder = st.empty()
main_holder = st.empty()

# What classes are available ?
available_classes = listdir("classes/")

##########################
# Student identification #
##########################
if "firstname" not in st.session_state:
    set_identification_form(title_holder, main_holder, available_classes)


# How many supports ?
if "support_number" in st.session_state:
    study_path = join("classes", st.session_state["selected_study"], "content.json")
    with open(study_path, "r") as json_file:
        st.session_state["content"] = json.load(json_file)
        st.session_state["support_count"] = len(st.session_state["content"])

    ##############
    # Side Panel #
    ##############
    set_side_panel_view()

    #############
    # Main Page #
    #############
    set_main_view(title_holder, main_holder)
