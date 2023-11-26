import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from frontend import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages: # loop through the pages to read the text
            text += page.extract_text() # extract text from the page
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000, # 1000 characters
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    #embeddings = OpenAIEmbeddings() # paid version
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if (i % 2 == 0):
            st.write(user_template.replace(
                "{{message}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{message}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Reading multiple PDFs", page_icon=":computer:")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Reading multiple PDFs")
    user_question = st.text_input("Ask a question about the documents you have uploaded:")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs and click Run", accept_multiple_files=True
        )
        if st.button("Run"):
            with st.spinner("Reading your PDFs... Please wait..."):
                print("triggered")
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                st.write(raw_text)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                #st.write()

                # create vector store
                vectorstore = get_vector_store(text_chunks)

                # create conversation chain (take history of the convo and use it to the next ele)
                st.session_state.conversation = get_conversation_chain(vectorstore) # persistent convo

if __name__ == '__main__':
    main()