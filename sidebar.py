import streamlit as st 
from faq import faq

def sidebar():
 with st.sidebar:
        st.sidebar.title("How to use")
        st.sidebar.write(
            " 1. Upload files📄\n"
            "2. Ask a question about the documents💬\n"
            "3. Get instant answers about your documents\n")


        #Sidebar Construction
        st.sidebar.markdown('______')
        st.sidebar.markdown('# About')
        st.sidebar.markdown(
            'ASTODOC📜 allows you to ask questions about your documents and get accurate answers with instant citations.')
        st.sidebar.markdown(
            'This tool is a work in progress.\n' 
            'You can contribute to the project on [LinkedIn](https://www.linkedin.com/posts/abdulkareemozovehe_astodoc-documentautomation-researchresources-activity-7072214864080850944-hH2X?utm_source=share&utm_medium=member_ios) with your feedback and suggestions💡')
        st.sidebar.markdown(
            'Developed by [Abdulkareem Ozovehe®](https://www.linkedin.com/in/abdulkareemozovehe/)'
        )
        st.sidebar.markdown('© 2023')
        st.sidebar.markdown('______')

        faq()