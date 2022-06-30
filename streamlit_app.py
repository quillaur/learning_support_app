import json
import streamlit as st
from os import walk


title_holder = st.empty()
main_holder = st.empty()

if "firstname" not in st.session_state:
    with main_holder.form("Identification"):
        firstname = st.text_input("Firstname:")
        lastname = st.text_input("Lastname:")
        classe = st.text_input("Your class:")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state["firstname"] = firstname
            st.session_state["lastname"] = lastname
            st.session_state["class"] = classe

if "firstname" in st.session_state and st.session_state["firstname"]:    
    main_holder.empty()

    support_number = 0
    for root, dirs, files in walk("supports"):
        support_number = len(files)

    if "support" not in st.session_state:
        st.session_state["support"] = 1
    
    with open(f"supports/page_{st.session_state['support']}.json", "r") as json_file:
        support = json.load(json_file)

    title_holder.title(support["title"])

    if support["link"]:
        main_holder.video(support["link"])
    
    elif support["text"]:
        main_holder.write(support["text"])

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["support"] > 1:
            prev = st.button("Previous")

            if prev:
                st.session_state["support"] -= 1
                st.experimental_rerun()

    with col2:
        if st.session_state["support"] < support_number:
            next = st.button("Next")

            if next:
                st.session_state["support"] += 1
                st.experimental_rerun()