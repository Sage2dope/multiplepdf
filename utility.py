import streamlit as st
from htmlTemplates import css, bot_template, user_template
from app import (get_conversation_chain, get_docx_text, get_pdf_text, get_text_chunks, get_vectorstore, handle_userinput, sidebar)






def main():  # sourcery skip: extract-method, use-named-expression
    
    st.set_page_config(page_title="astodoc",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
        st.session_state.chat_history = []

    with open('design.css') as source_des:
       st.markdown(f'<style>{source_des.read()}</style>', unsafe_allow_html= True)
    st.markdown("<h1 style= 'text-align: center:'>ASTODOC📓</h1>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload your Documents here and click on 'Process'",
        accept_multiple_files=True
    )

    if st.button('Process'):
          with st.spinner('Processing'):
                raw_pdf_text = ""
                raw_docx_text = ""
                unsupported_files = []


                for uploaded_file in uploaded_files:
                    if uploaded_file.type == 'application/pdf':
                        #process pdf file
                        pdf_text = get_pdf_text([uploaded_file])
                        raw_pdf_text += pdf_text
                    elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                        #Process docx files 
                        docx_text = get_docx_text([uploaded_file])
                        raw_docx_text += docx_text
                    else:
                        #Unsupported file type 
                        unsupported_files.append(uploaded_file.name)

                #Combine text from pdf and docx. files 
                raw_text = raw_pdf_text + raw_docx_text

                if unsupported_files:
                    unsupported_files_str = ", ".join(unsupported_files)
                    st.error(
                        f"Sorry, the following file(s) cannot be processed: {unsupported_files_str}. Please upload another file."
                    )
                else:



                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    if vectorstore is None:
                        #Error occured during processing 
                        return
                    else:
                        # create conversation chain
                        st.session_state.conversation = get_conversation_chain(
                            vectorstore)


    #Handling User Input 
    with st.form(key="user_input_form"):
        user_question = st.text_input("Ask any questions about your documents:")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not user_question:
                st.error("You have not entered a question. Please enter a question.")
            else:
                if st.session_state.conversation is None:
                    st.error("Conversation not initialized. Please upload and process documents first.")
                    return
                handle_userinput(user_question)
                st.empty()

    #Display Input History
    for _ in reversed(st.session_state.chat_history):
    #Clear Input History 
        st.session_state.chat_history = []

        
    #Sidebar structure
    sidebar()
