import streamlit as st
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
from zipfile import ZipFile
from math import ceil

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


    
def draw_certificat_info(img: Image) -> None:
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
    # Custom font style and font size
    font = font_manager.FontProperties(family='sans-serif', weight='bold')
    file = font_manager.findfont(font)
    font_size = 50
    myFont = ImageFont.truetype(file, font_size)
    txt = f"{st.session_state['firstname']} {st.session_state['lastname']}"
    # Adjust font size until it fits the box:
    while myFont.getsize(txt)[0] > 400:
        font_size -= 1
        myFont = ImageFont.truetype(file, font_size)

    # Add name of student to certificat
    color = (255, 255, 255)
    I1.text((615,210), txt, font=myFont, fill=color)

    # Add study name
    study_name = " ".join(st.session_state['selected_study'].split("_"))
    I1.text((615,365), study_name.capitalize(), font=myFont, fill=color)

    # Add score
    score_ratio = ceil((st.session_state["score"] / st.session_state["max_score"]) * 100) if st.session_state["max_score"] > 0 else 0
    I1.text((115,290), f"Success: {score_ratio}%", font=myFont, fill=color)


def draw_image(image_name: str) -> Image:
    # Images are all compressed in a zip file names 'ressources.zip'.
    resc_path = join(st.session_state["study_path"], "ressources.zip")
    with ZipFile(resc_path, "r") as myzip:
        with myzip.open(f"ressources/{image_name}") as img_file:
            img = Image.open(img_file)
            img.load()
    
            if "certificat" in image_name:
                draw_certificat_info(img)
    
    return img


@st.cache()
def prep_certif_for_download(img: Image) -> bytes:
    img_name ="prepared_certification.png"
    img.save(img_name)
    return img_name


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
                    if not "certificat" in v:
                        img = draw_image(v)
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
                        if len(this_page['answer']) > 1:
                            st.warning(f"The answers were: {', '.join(this_page['answer'])}")
                        else:
                            st.warning(f"The answer was: {', '.join(this_page['answer'])}")
                    else:
                        # Show the possible answers in a multiselect fassion.
                        resp = st.multiselect("Your answer:", options=this_page["possible answers"], default=None)

                        submit = st.button("Submit")
                        if submit:
                            resp.sort()
                            this_page["answer"].sort()
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
                    # The decision is based on whether or not your score is higher than a ratio defined by the teacher.
                    score_ratio = (st.session_state["score"] / st.session_state["max_score"]) * 100 if st.session_state["max_score"] > 0 else 0

                    # When this is the last page, you see if you can get a certification for this study or not.
                    score_msg = f"Your final score: {st.session_state['score']} / {st.session_state['max_score']} ({score_ratio}%)"

                    if score_ratio > v:
                        st.balloons()
                        st.success("Well done! You scored high enough to get this study certification !")

                        img = draw_image(this_page["image"])
                        img_name = prep_certif_for_download(img)

                        col1, col2 = st.columns([4,1])
                        with col1:
                            st.warning("Don't forget to download it !")   
                        with col2:          
                            with open(img_name, "rb") as bfile:
                                st.download_button(
                                    label="Download", 
                                    data=bfile,
                                    file_name=img_name,
                                    mime="image/png"
                                    )
                        
                        st.image(img)
                    else:
                        st.error(score_msg)
                        st.warning("Sorry, you did not score high enough to get this certification.")
                        st.info("Feel free to retry anytime !")
                