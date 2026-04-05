---
title: Attic Ai Challenge
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: 'an end-to-end Retrieval-Augmented Generation (RAG) system '
---
# Attic AI Challenge

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/sysharl/attic-ai-challenge)

This repository contains the **Attic AI Challenge** application. The project features a specialized **RAG (Retrieval-Augmented Generation)** pipeline, allowing users to upload documents and perform natural language queries to extract precise information.

---

## 🖥️ Frontend Overview

The application's frontend is built using **Streamlit**, providing a responsive interface tailored for document intelligence and conversational AI.
### Key Frontend Features:
* **Document-to-Query Interface:** A dedicated workspace to upload documents and interact with them using a RAG-based chat system.
* **Large File Support:** Configured to handle uploads up to **100MB**, suitable for extensive PDFs or technical documentation.
* **Source-Centric Design:** The UI logic is contained within the `src/` directory for better project organization.
---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* `pip` package manager

### Installation
#### 1. **Clone the repository:**
   ```bash
   git clone https://huggingface.co/spaces/sysharl/attic-ai-challenge
   cd attic-ai-challenge
   ```
#### 2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
#### 3. **Running the Application Locally**
 To launch the frontend with the necessary configurations for file handling, use the following command:

  ```bash
  streamlit run src/streamlit_app.py --server.maxUploadSize=100
  ```
### 🛠️ Project Structure
```plaintext
attic-ai-challenge/
├── src/
│   └── streamlit_app.py   # Main Frontend Application
├── requirements.txt       # Project Dependencies
└── README.md              # Documentation
```
### 📖 Usage
1. Start the Server: Execute the Streamlit run command in your terminal.
2. Access the UI: Open the local URL (usually http://localhost:8501) in your browser.
3. Upload Documents: Use the upload widget to ingest documents (up to 100MB).
4. Query: Enter your questions in the chat input to retrieve answers directly from the uploaded content.