import streamlit as st
from math import ceil

def previous_button() -> None:
    if st.session_state["support_number"] > 0:
        prev = st.button("Previous")

        if prev:
            st.session_state["support_number"] -= 1
            st.experimental_rerun()
    else:
        st.button("Previous", disabled=True)

def next_button() -> None:
    if st.session_state["support_number"] < st.session_state["support_count"]-1:
        next = st.button("Next")

        if next:
            st.session_state["support_number"] += 1
            st.experimental_rerun()
    else:
        st.button("Next", disabled=True)


def set_side_panel_view() -> None:
    st.sidebar.write(f"Firstname : {st.session_state['firstname']}")
    st.sidebar.write(f"lastname : {st.session_state['lastname']}")
    st.sidebar.write(f"Class : {st.session_state['class']}")
    st.sidebar.write(f"Study : {st.session_state['selected_study']}")
    st.sidebar.write("Study progress:")

    # For a nicer color for the progress bar:
    # https://discuss.streamlit.io/t/changing-each-progress-bar-to-different-colors/18827/3
    st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #99ff99 , #00ccff);
        }
    </style>""",
    unsafe_allow_html=True)
    st.sidebar.progress((st.session_state['support_number']+1) / st.session_state['support_count'])

    if st.session_state['delta'] == 0:
        st.sidebar.metric("Your score:", value=f"{st.session_state['score']} pts")
    else:
        st.sidebar.metric("Your score:", value=f"{st.session_state['score']} pts", delta=st.session_state['delta'])
    
    col1, col2 = st.sidebar.columns([3,1])
    with col1:
        previous_button()
    with col2:
        next_button()