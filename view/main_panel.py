import streamlit as st
from os.path import abspath
from PIL import Image


def set_main_view(title_holder: st.empty, main_holder: st.empty) -> None:
    main_holder.empty()
    
    this_page = st.session_state["content"][st.session_state["support_number"]]

    title_holder.title(this_page["title"])

    # 3 possible types of supports:
    if this_page["link"]:
        main_holder.video(this_page["link"])
    
    elif this_page["text"]:
        main_holder.write(this_page["text"])

    elif this_page["image"]:
        img_path = abspath(this_page["image"])
        main_holder.image(Image.open(img_path))
    
    # Is there a question to ask ?
    if this_page["question"]:
        main_holder.write(this_page["question"])

        with st.form("Answers"):
            resp = st.selectbox("Your answer:", options=this_page["possible answers"])

            submit = st.form_submit_button()
            if submit:
                if resp == this_page["answer"]:
                    st.success("Godd job ! This is correct.")
                else:
                    st.error(f"Sorry... The answer was: {this_page['answer']}")