import streamlit as st
import requests

API_URL = "https://sysharl.esmundo.dev"
# API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="PDF Q&A", layout="wide")

# -----------------------
# Session State Init
# -----------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------
# Title
# -----------------------
st.title("📄 Chat with your PDF")

# -----------------------
# Sidebar: Upload
# -----------------------
st.sidebar.header("Upload Document")

uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"], accept_multiple_files=True)
strategy = st.sidebar.selectbox("Chunking Strategy", ["recursive", "fixed"])

if st.sidebar.button("Upload"):
    if not uploaded_file:
        st.sidebar.error("Please upload a PDF first.")
    else:
        with st.spinner("Processing document..."):
            try:
                files = [
                    ("files", (f.name, f, "application/pdf")) for f in uploaded_file
                ]
                data = {"strategy": strategy}

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    data=data
                )

                if response.status_code == 200:
                    res = response.json()

                    files_result = res.get("files", [])

                    # Get only successful uploads
                    successful = [f for f in files_result if "session_id" in f]
                    failed = [f for f in files_result if "error" in f]

                    if not successful:
                        st.sidebar.error("❌ All files failed to process.")
                        for f in failed:
                            st.sidebar.write(f"**{f['file_name']}**: {f['error']}")
                    else:
                        # Use first successful session (or you can store all)
                        st.session_state.session_id = successful[0]["session_id"]
                        st.session_state.chat_history = []

                        st.sidebar.success(f"✅ {len(successful)} file(s) uploaded successfully!")

                        # Show successful files
                        for f in successful:
                            st.sidebar.write(f"✔ {f['file_name']}")

                        # Show failed files (if any)
                        if failed:
                            st.sidebar.warning("Some files failed:")
                            for f in failed:
                                st.sidebar.write(f"❌ {f['file_name']}: {f['error']}")

                else:
                    st.sidebar.error(response.json().get("detail", "Upload failed"))

            except Exception as e:
                print("Exception:", e)
                if 'response' in locals():
                    print("Response text:", response.text)
                st.sidebar.error("Could not connect to API.")

# -----------------------
# Main Chat Interface
# -----------------------
if not st.session_state.session_id:
    st.info("👈 Upload a PDF to start chatting")
    st.stop()

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

        # Show sources
        with st.expander("📌 Sources"):
            for src in chat["sources"]:
                st.markdown(f"**Page {src['page']}**")
                st.write(src["text"])
                st.divider()

# -----------------------
# User Input
# -----------------------
question = st.chat_input("Ask a question about your document...")
if question:
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "session_id": st.session_state.session_id,
                        "question": question
                    }
                )

                if response.status_code == 200:
                    res = response.json()
                    answer = res["answer"]
                    sources = res["sources"]
                    if answer == 'I cannot find this in the document.':
                        sources = []
                    st.markdown(answer)
                    if sources:
                        with st.expander("📌 View Source Chunks"):
                            for src in sources:
                                # Extract the source info we added in the backend
                                doc_name = src.get("source", "Unknown Document")
                                page_num = src.get("page", "N/A")
                                chunk_idx = src.get("chunk_index", "?")
                                chunk_text = src.get("text", "No content available.")

                                # Professional header showing Filename | Page | Chunk
                                st.markdown(f"**📄 {doc_name}**")
                                st.caption(f"Page {page_num} | Chunk Index {chunk_idx}")
                                
                                # Show the text snippet
                                st.write(chunk_text)
                                st.divider()

                    # Save to history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer,
                        "sources": sources
                    })

                else:
                    error_detail = response.json().get("detail", "Unknown error")
                    st.error(f"Backend Error: {error_detail}")

            except Exception as e:
                print("Exception:", e)
                st.error("Our document library is currently unreachable. We're working on restoring the link—please try your query again shortly")