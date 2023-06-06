import streamlit as st
from streamlit_option_menu import option_menu
from sidebar import faq, sidebar
from app import main

def navbar(navsystem):
    if navsystem == 1:
        selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Projects", "Contact"],  # required
                icons=["house", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {
                        "font-size": "25px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {"background-color": "green"},
                },
            )
        
        return selected
    

selected = navbar(navsystem= 1)

if selected == "Home":
    st.title(f"You have selected {main}")
if selected == "Projects":
    st.title(f"You have selected {sidebar}")
if selected == "Contact":
    st.title(f"You have selected {faq}")



