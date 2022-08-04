import streamlit as st

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
    st.sidebar.write(f"Page: {st.session_state['support_number']+1} / {st.session_state['support_count']}")
    st.sidebar.write(f"Good answers: {st.session_state['good_answers']} / {st.session_state['total_answers']}")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        previous_button()
    with col2:
        next_button()