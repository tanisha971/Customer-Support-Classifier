import streamlit as st

def initialize_state():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    if "history" not in st.session_state:
        st.session_state.history = []

    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    if "last_ticket" not in st.session_state:
        st.session_state.last_ticket = ""

    if "sample_index" not in st.session_state:
        st.session_state.sample_index = 0

def get_theme():
    if st.session_state.dark_mode:
        return {
            "mode": "dark",
            "bg": "#050914",
            "sidebar": "rgba(7, 15, 31, 0.82)",
            "surface": "rgba(16, 29, 53, 0.58)",
            "surface_strong": "rgba(15, 27, 49, 0.82)",
            "input": "rgba(5, 13, 27, 0.72)",
            "text": "#F4F7FF",
            "muted": "#A2B1CC",
            "border": "rgba(126, 166, 255, 0.20)",
            "blue": "#398BFF",
            "blue2": "#655BFF",
            "cyan": "#46D7FF",
            "shadow": "0 18px 55px rgba(0, 0, 0, 0.30)",
            "result": "rgba(26, 72, 135, 0.30)",
            "chart": "#398BFF",
        }

    return {
        "mode": "light",
        "bg": "#EEF4FF",
        "sidebar": "rgba(255, 255, 255, 0.76)",
        "surface": "rgba(255, 255, 255, 0.68)",
        "surface_strong": "rgba(255, 255, 255, 0.88)",
        "input": "rgba(255, 255, 255, 0.82)",
        "text": "#14213A",
        "muted": "#63728D",
        "border": "rgba(61, 112, 205, 0.18)",
        "blue": "#176BFF",
        "blue2": "#735BFF",
        "cyan": "#00A9D6",
        "shadow": "0 18px 50px rgba(40, 75, 140, 0.10)",
        "result": "rgba(219, 234, 255, 0.72)",
        "chart": "#176BFF",
    }
