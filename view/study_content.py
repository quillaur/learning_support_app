import streamlit as st
from os.path import join
from PIL import Image
from zipfile import ZipFile
import json


def draw_image(image_name: str) -> Image:
    # Images are all compressed in a zip file names 'ressources.zip'.
    resc_path = join(st.session_state["study_path"], "ressources.zip")
    with ZipFile(resc_path, "r") as myzip:
        with myzip.open(f"{image_name}") as img_file:
            img = Image.open(img_file)
            img.load()
    
    return img

def show_question(q: dict):
    col1, col2 = st.columns(2, gap="large")
    with col1:
        for k, v in q.items():
            if v: 
                if k == "title":
                    st.subheader(v)
                
                elif k.startswith("text"):
                    st.info(v)
                
                elif k.startswith("image"):
                    if "https" in v:
                        st.image(v)
                    elif not "certificat" in v:
                        img = draw_image(v)
                        st.image(img)
                elif k == "question":
                    st.write(v)
    with col2:
        answer_count = len(['answer'])
        if answer_count > 1:
            resp = st.multiselect("Your answer(s): (several answers are possible)", options=q["possible answers"], default=None, key=q["id"])
        else:
            resp = st.selectbox("Your answer:", options=[None]+q["possible answers"], key=q["id"])
            resp = [resp]
            
    st.write("-----------------")


def set_quiz_view():
    quiz_path = join(st.session_state["study_path"], "quiz.json")
    with open(quiz_path, "r") as json_file:
        questions = json.load(json_file)

    
    with st.form("answer select"):
        for q in questions:
            show_question(q)
        
        submit = st.form_submit_button()
        if submit:
            pass


def set_main_view() -> None:
    """
    The layout of the main view must be dynamicaly updated based on the content.json file.
    It must contain a title and then either texts, images or videos 
    in the order given by the content file.
    """
    # I empty again the main holder because sometimes (and for unknown reasons...) 
    # it is not fully emptied at this point.
    study_path = join(st.session_state["study_path"], "content.json")
    with open(study_path, "r") as json_file:
        st.session_state["content"] = json.load(json_file)

    content_parts = list(st.session_state["content"].keys()) + ["Quiz"]

    tabulations = st.tabs(content_parts)

    for i, tab in enumerate(tabulations):
        with tab:
            # For each element in this page (a dictionnary).
            # for title, this_page in st.session_state["content"].items():
            #     if st.session_state[title]:
            tab_title = content_parts[i]

            if tab_title == "Quiz":
                set_quiz_view()
            else:
                this_page = st.session_state["content"][tab_title]
                col1, col2 = st.columns(2, gap="large")
                with col1:
                    st.title(tab_title)
                    # If there is a value for this element, 
                    # it means the creator wants it to be on the page.
                    for k, v in this_page.items():
                        if v:                               
                            # There can be several text keys.
                            if k.startswith("text"):
                                st.info(v)
                            
                            elif k == "video_source" or k == "source_image":
                                st.info(f"Source: {v}")
                            
                
                with col2:
                    for k, v in this_page.items():
                        if v:
                            if k == "video_url":
                                if "video_start" in this_page and this_page["video_start"]:
                                    start_time = this_page["video_start"]
                                else:
                                    start_time = 0

                                st.video(v, start_time=start_time)

                            # There can be several image keys.
                            elif k.startswith("image"):
                                if "https" in v:
                                    st.image(v)
                                elif not "certificat" in v:
                                    img = draw_image(v)
                                    st.image(img)

            # st.write("-----------------")

                            