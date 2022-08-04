from os.path import join
import streamlit as st
import json


def load_study_content() -> None:
    study_path = join(st.session_state["study_path"], "content.json")
    with open(study_path, "r") as json_file:
        st.session_state["content"] = json.load(json_file)
        st.session_state["support_count"] = len(st.session_state["content"])
        st.session_state["pages_done"] = [False] * st.session_state["support_count"]
        st.session_state["good_answers"] = 0 
        st.session_state["total_answers"] = 0 