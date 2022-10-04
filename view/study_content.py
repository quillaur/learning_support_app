import streamlit as st
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from matplotlib import font_manager
from zipfile import ZipFile
from math import ceil
import json

def adapt_string_to_font(txt: str, myFont: ImageFont) -> str:
    return txt if myFont.getsize(txt)[0] < 400 else "\n".join(txt.split())

    
def draw_certificat_info(img: Image) -> None:
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
    # Custom font style and font size
    font = font_manager.FontProperties(family='cursive', weight='bold')
    file = font_manager.findfont(font)
    font_size = 45
    myFont = ImageFont.truetype(file, font_size)
    txt = f"{st.session_state['firstname']} {st.session_state['lastname']}"
    txt = adapt_string_to_font(txt, myFont)

    # Add name of student to certificat
    color = (255, 255, 255)
    
    I1.text((800,230), txt, font=myFont, fill=color, anchor="mm", align='center')

    # Add study name
    txt = adapt_string_to_font(st.session_state['selected_study'], myFont)
    I1.text((800,395), txt, font=myFont, fill=color, anchor="mm", align='center')

    # Add score
    score_ratio = st.session_state["score"]
    # score_ratio = 80
    txt = f"Success: {score_ratio}%"
    I1.text((260,315), txt, font=myFont, fill=color, anchor="mm", align='center')



def draw_image(image_name: str) -> Image:
    # Images are all compressed in a zip file names 'ressources.zip'.
    resc_path = join(st.session_state["study_path"], "ressources.zip")
    with ZipFile(resc_path, "r") as myzip:
        with myzip.open(f"{image_name}") as img_file:
            img = Image.open(img_file)
            img.load()

            if "certificat" in image_name:
                draw_certificat_info(img)
    
    
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
            st.multiselect("Your answer(s): (several answers are possible)", options=q["possible answers"], default=None, key=q["id"])
        else:
            st.radio("Your answer:", options=[None]+q["possible answers"], key=q["id"])
            
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
            good_answer = 0
            max_points = len(questions)
            for q in questions:
                q["answer"].sort()

                for k, v in st.session_state.items():
                    if k == q["id"]:
                        if isinstance(v, list):
                            v.sort()
                            if q["answer"] == v:
                                good_answer += 1
                        elif q["answer"][0] == v:
                            good_answer += 1
            
            st.session_state["score"] = ceil(good_answer / max_points * 100)

            st.info("Click on the certificat tab to see your final score !")

@st.cache()
def prep_certif_for_download(img: Image) -> bytes:
    img_name ="prepared_certification.png"
    img.save(img_name)
    return img_name


def set_certificat_view():
    if st.session_state["score"] == 0:
        st.info("You need to submit your answers to the quiz to get a certificat of completion.") 
    elif st.session_state["score"] < 50:
        st.error(f"Your score: {st.session_state['score']*100} / 100")
        st.warning("Sorry, you did not score high enough to get this certification.")
        st.info("Feel free to retry anytime !")
    else:
        st.balloons()
        with st.form("Identification"):
            st.success("Well done! You scored high enough to get this study certification !")
            st.warning("Enter your name and download your personal certification !")

            col1, col2 = st.columns(2)
            with col1:
                firstname = st.text_input("Firstname:")
            with col2:
                lastname = st.text_input("Lastname:")
    
            submit = st.form_submit_button()
            
            if submit:
                st.session_state['firstname'] = firstname
                st.session_state['lastname'] = lastname
        
        if "firstname" in st.session_state:
            img = draw_image("certificat.png")
            img_name = prep_certif_for_download(img)

            col1, col2 = st.columns([2,1])
            with col1:
                st.image(img)
            with col2:          
                st.warning("Don't forget to download it !")   
                with open(img_name, "rb") as bfile:
                    st.download_button(
                        label="Download Your Certificat", 
                        data=bfile,
                        file_name=img_name,
                        mime="image/png"
                        )



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

    content_parts = list(st.session_state["content"].keys()) + ["Quiz", "Certificat"]

    tabulations = st.tabs(content_parts)

    for i, tab in enumerate(tabulations):
        with tab:
            # For each element in this page (a dictionnary).
            # for title, this_page in st.session_state["content"].items():
            #     if st.session_state[title]:
            tab_title = content_parts[i]

            if tab_title == "Quiz":
                set_quiz_view()
            elif tab_title == "Certificat":
                set_certificat_view()
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

                            