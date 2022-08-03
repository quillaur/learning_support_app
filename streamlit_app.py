import json
import streamlit as st
import os
from PIL import Image

title_holder = st.empty()
main_holder = st.empty()

# What classes are available ?
available_classes = os.listdir("classes/")

##########################
# Student identification #
##########################
if "firstname" not in st.session_state:
    with main_holder.form("Identification"):
        firstname = st.text_input("Firstname:")
        lastname = st.text_input("Lastname:")
        your_class = st.text_input("Your class:")
        selected_study = st.selectbox("Please select what you would like to study:", available_classes)

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["firstname"] = firstname
            st.session_state["lastname"] = lastname
            st.session_state["class"] = your_class
            st.session_state["selected_study"] = selected_study
            st.session_state["support_number"] = 0


# How many supports ?
if "support_number" in st.session_state:
    study_path = os.path.join("classes", st.session_state["selected_study"], "content.json")
    with open(study_path, "r") as json_file:
        st.session_state["content"] = json.load(json_file)
        st.session_state["support_count"] = len(st.session_state["content"])

    ##############
    # Side Panel #
    ##############
    st.sidebar.write(f"Firstname : {st.session_state['firstname']}")
    st.sidebar.write(f"lastname : {st.session_state['lastname']}")
    st.sidebar.write(f"Class : {st.session_state['class']}")
    st.sidebar.write(f"Selected study : {st.session_state['selected_study']}")

    #############
    # Main Page #
    #############

    main_holder.empty()
    
    this_page = st.session_state["content"][st.session_state["support_number"]]

    title_holder.title(this_page["title"])

    # 3 possible types of supports:
    if this_page["link"]:
        main_holder.video(this_page["link"])
    
    elif this_page["text"]:
        main_holder.write(this_page["text"])

    elif this_page["image"]:
        img_path = os.path.abspath(this_page["image"])
        main_holder.image(Image.open(img_path))
    
    # Is there a question to ask ?
    if this_page["question"]:
        main_holder.write(this_page["question"])

        col1, col2 = st.columns(2)
        with col1:
            resp = st.button(this_page["r1"])
            resp = st.button(this_page["r3"])
        with col2:
            resp = st.button(this_page["r2"])
            resp = st.button(this_page["r4"])
        
        if resp and resp == this_page["r"]:
            st.success("Godd job ! This is correct.")
        elif resp:
            st.error(f"Sorry... The answer was: {this_page['r']}")

    col1, col2 = st.columns([10,1])
    with col1:
        if st.session_state["support_number"] > 0:
            prev = st.button("Previous")

            if prev:
                st.session_state["support_number"] -= 1
                st.experimental_rerun()
        else:
            st.button("Previous", disabled=True)

    with col2:
        if st.session_state["support_number"] < st.session_state["support_count"]-1:
            next = st.button("Next")

            if next:
                st.session_state["support_number"] += 1
                st.experimental_rerun()
        else:
            st.button("Next", disabled=True)