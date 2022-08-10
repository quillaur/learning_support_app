import streamlit as st
from math import ceil

def previous_button() -> None:
    """
    Create a button that decrement the suport number value 
    in the streamlit session state object.
    """
    # If this is not the first app page.
    if st.session_state["support_number"] > 0:
        prev = st.button("Previous")

        if prev:
            # Decrement the page number.
            st.session_state["support_number"] -= 1
            # Refresh the page to take the change of state into account.
            st.experimental_rerun()
    else:
        # If it is the first page, disable the button.
        st.button("Previous", disabled=True)

def next_button() -> None:
    """
    Create a button that increment the suport number value 
    in the streamlit session state object.
    """
    # If this is not the last app page.
    if st.session_state["support_number"] < st.session_state["support_count"]-1:
        next = st.button("Next")

        if next:
            # Increment the page number.
            st.session_state["support_number"] += 1
            # Refresh the page to take the change of state into account.
            st.experimental_rerun()
    else:
        # If it is the last page, disable the button.
        st.button("Next", disabled=True)


def set_side_panel_view() -> None:
    """
    This function defines the layout of the side panel.
    """
    # The title is the name of the study.
    study_name = " ".join(st.session_state['selected_study'].split("_"))
    st.sidebar.title(f"{study_name.capitalize()}")

    # # Show the student caracteristics.
    # st.sidebar.write(f"Firstname : {st.session_state['firstname']}")
    # st.sidebar.write(f"lastname : {st.session_state['lastname']}")
    # st.sidebar.write(f"Class : {st.session_state['class']}")
    
    # Add a progress bar to indicate where we are in the study.
    progress = ceil((st.session_state['support_number']+1) / st.session_state['support_count']*100)
    st.sidebar.write(f"Study progress: {progress} %")
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
    st.sidebar.progress(progress)

    # Add a slider for page debug purpose.
    st.session_state['support_number'] = st.sidebar.slider("Select a page:", 1, st.session_state['support_count'], st.session_state['support_number']+1) - 1

    # Add a metric to indicate the score of the student.
    # The delta shows how many points on a row were lost or gained.
    if st.session_state['delta'] == 0:
        st.sidebar.metric("Your score:", value=f"{st.session_state['score']} pts")
    else:
        st.sidebar.metric("Your score:", value=f"{st.session_state['score']} pts", delta=st.session_state['delta'])
    
    # Place the previous and next button.
    col1, col2 = st.sidebar.columns([3,1])
    with col1:
        previous_button()
    with col2:
        next_button()