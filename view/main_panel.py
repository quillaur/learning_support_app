import streamlit as st
from os.path import join
from PIL import Image


def set_main_view(main_holder: st.empty) -> None:
    
    this_page = st.session_state["content"][st.session_state["support_number"]]

    with main_holder.container():
        st.title(this_page["title"])

        # 3 possible types of supports:
        if this_page["text"]:
            st.info(this_page["text"])
        
        if this_page["video_url"]:
            st.video(this_page["video_url"])

        if this_page["image"]:
            img_path = join(st.session_state["study_path"], this_page["image"])
            st.image(Image.open(img_path))

        # Is there a question to ask ?
        if this_page["question"]:
            st.write(this_page["question"])

            if st.session_state["pages_done"][st.session_state["support_number"]]:
                st.warning(f"This answer was: {this_page['answer']}")
            else:
                resp = st.selectbox("Your answer:", options=this_page["possible answers"])
                submit = st.button("Submit")
            
                if submit:
                    if resp == this_page["answer"]:
                        st.success("Good job ! This is correct.")
                        st.session_state["score"] += 1
                        if st.session_state["delta"] >= 0:
                            st.session_state["delta"] += 1
                        else:
                            st.session_state["delta"] = 1
                    else:
                        st.error(f"Sorry... The answer was: {this_page['answer']}")
                        st.session_state["score"] -= 1

                        if st.session_state["delta"] <= 0:
                            st.session_state["delta"] -= 1
                        else:
                            st.session_state["delta"] = -1
                    
                    st.session_state["pages_done"][st.session_state["support_number"]] = True
                