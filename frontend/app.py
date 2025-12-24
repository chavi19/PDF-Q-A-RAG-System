import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="PDF Q&A", layout="wide")
st.title("📄 PDF Question Answering")

# Initialize session
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

# Upload section
st.subheader("1️⃣ Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

if uploaded_file and st.button("Process PDF"):
    with st.spinner("Processing..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ {data['message']}")
                st.info(f"📄 File: {data['filename']} | Chunks: {data['chunks']}")
                st.session_state.uploaded = True
            else:
                st.error(f"Error: {response.json()}")
        except Exception as e:
            st.error(f"Error: {e}")

# Question section
if st.session_state.uploaded:
    st.subheader("2️⃣ Ask Question")
    question = st.text_input("Your question")
    
    if st.button("Get Answer"):
        if question:
            with st.spinner("Generating answer..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        json={"question": question},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.subheader("🤖 Answer")
                        st.write(data["answer"])
                        st.caption(f"Source: {data['source']}")
                    else:
                        st.error(f"Error: {response.json()}")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question")