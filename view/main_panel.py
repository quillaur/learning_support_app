import streamlit as st
from os.path import join
from PIL import Image


def set_main_view(main_holder: st.empty) -> None:
    
    this_page = st.session_state["content"][st.session_state["support_number"]]

    with main_holder.container():
        st.title(this_page["title"])

        # 3 possible types of supports:
        if this_page["link"]:
            st.video(this_page["link"])

        elif this_page["text"]:
            st.write(this_page["text"])

        elif this_page["image"]:
            img_path = join(st.session_state["study_path"], this_page["image"])
            st.image(Image.open(img_path))

        # Is there a question to ask ?
        if this_page["question"]:
            st.write(this_page["question"])

            with st.form("Answers"):
                resp = st.selectbox("Your answer:", options=this_page["possible answers"])

                if st.form_submit_button():
                    if resp == this_page["answer"]:
                        st.success("Godd job ! This is correct.")
                    else:
                        st.error(f"Sorry... The answer was: {this_page['answer']}")