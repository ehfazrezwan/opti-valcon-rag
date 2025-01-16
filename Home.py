import streamlit as st
from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete
import os
import tempfile
from data_ingestor import ingest_data
from pathlib import Path

# Set page config
st.set_page_config(page_title="Optimizely VC Chat", page_icon="💬", layout="wide")

WORKING_DIR = "./rag_storage/valcon-data"
UPLOAD_DIR = "./data/knowledge-base/uploaded-files"

# Create upload directory if it doesn't exist
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


# Initialize LightRAG
@st.cache_resource
def init_rag():
    return LightRAG(working_dir=WORKING_DIR, llm_model_func=gpt_4o_mini_complete)


# Set up the Streamlit page
st.title("Optimizely Case Study Chat")
with open("intro.md", "r") as f:
    intro_content = f.read()
st.markdown(intro_content)
st.page_link("pages/1_Knowledge_Graph.py", label="View Knowledge Graph", icon="1️⃣")
st.page_link("pages/2_Example_QA.py", label="Example chat", icon="2️⃣")

# Initialize the RAG instance
rag = init_rag()

# Handle file uploads
uploaded_files = st.sidebar.file_uploader(
    "Upload a new file/new files into knowledge base.",
    accept_multiple_files=True,
)

st.sidebar.info(
    "Please note that file upload might take a while (depending on the length of the data) as they are ingested into the Knowledge Graph."
)

if uploaded_files:
    uploaded_paths = []
    for uploaded_file in uploaded_files:
        # Save uploaded file to the upload directory
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        uploaded_paths.append(file_path)

    # Display spinner while ingesting the uploaded files
    with st.spinner("Ingesting files..."):
        ingest_data(rag, [UPLOAD_DIR])

    st.sidebar.success(f"Successfully ingested {len(uploaded_files)} file(s)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = rag.query(prompt, param=QueryParam(mode="hybrid"))
        st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
