import streamlit as st
from os.path import join
from PIL import Image
from zipfile import ZipFile


def update_score(user_answer: str, good_answer: str) -> None:
    """
    Update the score and delta values of the session state object.

    Args:
        - user_answer: answer given by the user to the question.
        - good_answer: the right answer to the question provided by the teacher in the content.json file.
    """
    if user_answer == good_answer:
        st.success("Good job ! This is correct.")
        st.session_state["score"] += 1
        if st.session_state["delta"] >= 0:
            st.session_state["delta"] += 1
        else:
            st.session_state["delta"] = 1
    else:
        st.error(f"Sorry... The answer was: {good_answer}")
        st.session_state["score"] -= 1
        if st.session_state["delta"] <= 0:
            st.session_state["delta"] -= 1
        else:
            st.session_state["delta"] = -1

    



def set_main_view(main_holder: st.empty) -> None:
    """
    Once the student identification is done and a study has been selected, 
    the app show what I call the 'main' view.
    The layout of the main view must be dynamicaly updated based on the content.json file.
    It must contain a title and then either texts, images or videos 
    in the order given by the content file.
    """
    # Get the content of this specific page using 
    # the support number key of the session state object.
    this_page = st.session_state["content"][st.session_state["support_number"]]

    # I empty again the main holder because sometimes (and for unknown reasons...) 
    # it is not fully emptied at this point.
    main_holder.empty()
    with main_holder.container():
        # For each element in this page (a dictionnary).
        for k, v in this_page.items():
            # If there is a value for this element, 
            # it means the creator wants it to be on the page.
            if v:
                if k == "title":
                    st.title(v)

                # 3 possible types of supports:        
                elif k == "video_url":
                    st.video(v)

                # There can be several image keys.
                elif k.startswith("image"):
                    # Images are all compressed in a zip file names 'ressources.zip'.
                    resc_path = join(st.session_state["study_path"], "ressources.zip")
                    with ZipFile(resc_path, "r") as myzip:
                        with myzip.open(f"ressources/{v}") as img_file:
                            img = Image.open(img_file)
                            st.image(img)
                
                # There can be several text keys.
                elif k.startswith("text"):
                    st.info(v)

                # Is there a question to ask ?
                elif k == "question":
                    st.write(v)

                    # If the question has already been seen during this session, 
                    # just show the answer of the question. 
                    # Make it impossible for the user to answer several times to the same question.
                    if st.session_state["pages_done"][st.session_state["support_number"]]:
                        st.warning(f"This answer was: {this_page['answer']}")
                    else:
                        # Show the possible answers in a multiselect fassion.
                        resp = st.multiselect("Your answer:", options=this_page["possible answers"])

                        submit = st.button("Submit")
                        if submit:
                            update_score(resp, this_page["answer"])
                            
                            st.session_state["max_score"] += 1
                            st.session_state["pages_done"][st.session_state["support_number"]] = True
                
                elif k == "certif_ratio":
                    st.header(f"Your final score: {st.session_state['score']} / {st.session_state['max_score']}")

                    score_ratio = (st.session_state["score"] / st.session_state["max_score"]) * 100

                    if score_ratio > v:
                        st.balloons()
                        st.success("Well done! You scored high enough to get this study certification !")
                    else:
                        st.error("Sorry, you did not score high enough to get this certification.")
                        st.info("Feel free to retry anytime !")
                