import streamlit as st
from app import get_pdf_text, get_docx_text, get_conversation_chain, get_text_chunks, get_vectorstore 




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

                    if vectorstore is not None:
                              # create conversation chain
                              st.session_state.conversation = get_conversation_chain(
                                  vectorstore)