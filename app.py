import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from faq import faq
import tiktoken
import docx2txt
import openai





def get_docx_text(docx_file):
    if isinstance(docx_file, list):
        docx_file = docx_file[0]
    # Process the docx file and return the extracted text
    text = docx2txt.process(docx_file)
    return text




def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):  # sourcery skip: inline-immediately-returned-variable
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    # sourcery skip: inline-immediately-returned-variable
    embeddings = OpenAIEmbeddings()

    try:
        # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectorstore
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")
        return None


def get_conversation_chain(vectorstore):
    # sourcery skip: inline-immediately-returned-variable
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    try:
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history'][::-1]

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)       
            else:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
    except openai.error.InvalidRequestError as e:
        st.error("Document is too large. Please upload a smaller document.")



def main():  # sourcery skip: extract-method, use-named-expression
    
    st.set_page_config(page_title="astodoc",
                       page_icon=":books:")
    st.markdown(
        """
        <style>
        .header {
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            /* Add any other CSS properties or effects you desire */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
        st.session_state.chat_history = []

    st.markdown('<h1 class="header-text">ASTODOC :books:</h1>', unsafe_allow_html=True)

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
            'ASTODOC📜 allows you to ask questions about your documents'
            'and get accurate answers with instant citations.')
        st.sidebar.markdown(
            'This tool is a work in progress.\n' 
            'You can contribute to the project on [LinkedIn](https://www.linkedin.com/in/abdulkareemozovehe/) with your feedback and suggestions💡')
        st.sidebar.markdown(
            'Developed by [Abdulkareem Ozovehe®](https://www.linkedin.com/in/abdulkareemozovehe/)'
        )
        st.sidebar.markdown('© 2023')
        st.sidebar.markdown('______')

        faq()




def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))

num_tokens_from_string("tiktoken is great!", "cl100k_base")


if __name__ == '__main__':
    main()


# Display the HTML file with the JavaScript code
with open("index.html", "r") as file:
    st.markdown(file.read(), unsafe_allow_html=True)
