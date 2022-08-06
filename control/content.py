from os.path import join
import streamlit as st
import json

@st.cache()
def load_study_content() -> None:
    """
    Using the streamlit session_state object, 
    this function load the selected study content as a list of dictionnaries. 
    Content is then inserted in the session_state object to keep it available 
    even upon page refresh.
    """
    study_path = join(st.session_state["study_path"], "content.json")
    with open(study_path, "r") as json_file:
        st.session_state["content"] = json.load(json_file)
        st.session_state["support_count"] = len(st.session_state["content"])
        st.session_state["pages_done"] = [False] * st.session_state["support_count"]
        st.session_state["score"] = 0
        st.session_state["max_score"] = 0
        st.session_state["delta"] = 0 