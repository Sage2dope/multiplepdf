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
from utility import main
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

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )
    return conversation_chain


def handle_userinput(user_question):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    response = st.session_state.conversation({'question': user_question, 'chat_history': st.session_state.chat_history})
    st.session_state.chat_history = response['chat_history']

    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)



main()



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
    
