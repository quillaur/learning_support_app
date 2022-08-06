import streamlit as st
from os.path import join
from PIL import Image
from zipfile import ZipFile

def update_delta(positif: bool) -> None:
    """
    Update the delta value of the session state object.

    Args:
        - positif: bool indicatating if increment (True) or decrement (False) is needed.
    """
    if positif:
        if st.session_state["delta"] >= 0:
            st.session_state["delta"] += 1
        else:
            st.session_state["delta"] = 1
    else:
        if st.session_state["delta"] <= 0:
            st.session_state["delta"] -= 1
        else:
            st.session_state["delta"] = -1


def update_score(positif: bool) -> None:
    """
    Update the score value of the session state object.

    Args:
        - positif: bool indicatating if increment (True) or decrement (False) is needed.
    """
    if positif:
        st.session_state["score"] += 1
    else:
        st.session_state["score"] -= 1


    



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
                            good_answer: bool = resp == this_page["answer"]
                            update_score(good_answer)
                            update_delta(good_answer)

                            if good_answer:
                                st.success("Good job ! This is correct.")
                            else:
                                st.error(f"Sorry... The answer was: {this_page['answer']}")
                            
                            st.session_state["max_score"] += 1
                            st.session_state["pages_done"][st.session_state["support_number"]] = True
                
                elif k == "certif_ratio":
                    # When this is the last page, you see if you can get a certification for this study or not.
                    st.header(f"Your final score: {st.session_state['score']} / {st.session_state['max_score']}")

                    # The decision is based on whether or not your score is higher than a ratio defined by the teacher.
                    score_ratio = (st.session_state["score"] / st.session_state["max_score"]) * 100

                    if score_ratio > v:
                        st.balloons()
                        st.success("Well done! You scored high enough to get this study certification !")
                    else:
                        st.error("Sorry, you did not score high enough to get this certification.")
                        st.info("Feel free to retry anytime !")
                