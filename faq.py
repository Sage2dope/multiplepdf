import streamlit as st

def faq():
    st.sidebar.markdown(
        '# FAQ')
    
    st.sidebar.markdown(

        '## How does PDF Guru work?')
    st.sidebar.markdown(
        'When you upload a document, it gets split into smaller parts and stored in a special kind of database known as a vector index. This type of database enables you to search and find documents based on their meaning.\n')
    st.sidebar.markdown(
        'When you ask a question, PDF Guru will search for the most relevant information by looking through the smaller parts of the documents stored in the vector index. After finding the relevant chunks, PDF Guru will utilize GPT3 to generate a final answer for you.')
    
    st.sidebar.markdown(
        '## Is my data safe?')
    st.sidebar.markdown(
        'Yes, your data is secure. PDF Guru does not keep your documents or questions stored. Once you close the browser tab, all the data you upload is deleted.')
    
    st.sidebar.markdown(

        '## Why does it take so long to index my document?')
    st.sidebar.markdown(
        'If you are using a free API key from PDF Guru, it might take some time for your document to be indexed. This is because the free API key has certain limitations called rate limits. To make the indexing process faster, you have the option to use a paid API key.')
    
    st.sidebar.markdown(

        '## Are the answers accurate?')
    st.sidebar.markdown(
        'PDF Guru is generally accurate, but it is important to verify answers with reliable sources. However, there may be occasional inaccuracies due to the use of the GPT-3 model.\n'
        'PDF Guru search is based on relevance, so as the library continue to be updated, it may not find all the information or answer certain types of questions that require extensive context.'
    )