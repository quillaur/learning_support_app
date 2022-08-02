import json
import streamlit as st


# How many supports ?
if not "support_number" in st.session_state:
    with open("supports\content.json", "r") as json_file:
        st.session_state["content"] = json.load(json_file)
        st.session_state["support_count"] = len(st.session_state["content"])

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

    if "support_number" not in st.session_state:
        st.session_state["support_number"] = 0
    
    support = st.session_state["content"][st.session_state["support_number"]]

    title_holder.title(support["title"])

    if support["link"]:
        main_holder.video(support["link"])
    
    elif support["text"]:
        main_holder.write(support["text"])

    col1, col2 = st.columns(2)
    with col1:
        if st.session_state["support_number"] > 0:
            prev = st.button("Previous")

            if prev:
                st.session_state["support_number"] -= 1
                st.experimental_rerun()

    with col2:
        if st.session_state["support_number"] < st.session_state["support_count"]-1:
            next = st.button("Next")

            if next:
                st.session_state["support_number"] += 1
                st.experimental_rerun()