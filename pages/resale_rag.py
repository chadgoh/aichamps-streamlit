import streamlit as st
__import__('pysqlite3')
import sys

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate

# from utility import check_password

# if not check_password():
#     st.stop()
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
with st.expander("Important notice"):
    st.write('''
       IMPORTANT NOTICE: This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

        Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

        Always consult with qualified professionals for accurate and personalized advice.
    ''')

if st.secrets["OPENAI_API_KEY"] is None or st.secrets["OPENAI_API_KEY"] == "":
    print("OPENAI_API_KEY is not set")
    exit(1)
else:
    print("OPENAI_API_KEY is set")

# Initialize an empty list to hold all document chunks
merged_doc = []

# pattern for a mix of structured headings, lists, and pages, this pattern combines multiple options.
pattern = "(?<!\.\s)(\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b)\s*\n"

# Set up the text splitter with the desired chunking configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=100, 
    length_function=len, 
    is_separator_regex=True,
    separators=[pattern]
)

FOLDER_PATH = "./data"

# Iterate through all files in the specified folder
for file_name in os.listdir(FOLDER_PATH):
    if file_name.endswith(".pdf"):  # Check if the file is a PDF
        file_path = os.path.join(FOLDER_PATH, file_name)
        
        # Load and split the document
        loader = PyPDFLoader(file_path)
        doc_chunks = loader.load_and_split(text_splitter)
        
        # Add the document chunks to the merged document
        merged_doc.extend(doc_chunks)




embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = Chroma.from_documents(
    collection_name="hdb_resale_pdf_data",
    documents=merged_doc,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not neccesary
)



print("building prompt template...")
# Build prompt with refinement
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Where possible, use lists and tables to make things clearer. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)


# retriever
retriever_w_threshold = vector_store.as_retriever(
       search_type="mmr",
        similarity_threshold=0.8, 
        k=10 
    )


print("building qa chain...")
qa_chain = RetrievalQA.from_chain_type(
    ChatOpenAI(model='gpt-4o-mini'),
    retriever=retriever_w_threshold,
    return_source_documents=True, # Make inspection of document possible
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)



print("initiating chat history...")
# init chat history
if "messages" not in st.session_state:
    st.session_state.messages =[]


# display chat message history on app rerun 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


print("creating prompt")
# chat input bar
prompt = st.chat_input("Hello, ask me anything regarding HDB resale processes")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = qa_chain.invoke(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write(response.get("result"))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.get("result")})


