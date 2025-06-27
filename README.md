
# ⚖️ LegalSense – AI-Powered Legal Document Assistant

**LegalSense** is a lightweight, privacy-first AI assistant that enables users to upload legal PDFs and ask natural language questions. It uses domain-specific embeddings from **LegalBERT**, stores them in **ChromaDB**, and returns context-aware answers. Built using **FastAPI**, **PyMuPDF**, and a minimal **HTML/CSS interface**, LegalSense ensures that all uploaded documents and their embeddings are automatically deleted after the session ends.

---

## 🚀 Features

- 📄 Upload and parse legal PDFs
- 🧠 Generate embeddings using LegalBERT (`nlpaueb/legal-bert-base-uncased`)
- 🔍 Store and search chunks via **ChromaDB**
- 💬 Ask plain English questions and get accurate, context-rich answers
- 🔐 **Session-based privacy** — all files and vectors are deleted after session ends
- 🌐 Simple frontend (HTML + CSS, no JavaScript)

---

## 🧱 Architecture

```
User
 │
 ▼
[Frontend: index.html + style.css]
 │
 ▼
FastAPI Backend (main.py)
 ├── PDF Parsing         →  pdf_utils.py
 ├── Embedding           →  embedding_utils.py
 ├── Vector Store        →  vectorstore_utils.py
 ├── LLM Response        →  llm_utils.py
 ├── Session Handling    →  session_utils.py
 │
 ▼
Response (HTML Render)
```

---

## 📁 Project Structure

```
LegalSense/
├── main.py                    # FastAPI app and routing
├── embedding_utils.py         # Embedding logic using LegalBERT
├── vectorstore_utils.py       # ChromaDB utilities
├── pdf_utils.py               # PDF parsing using PyMuPDF
├── llm_utils.py               # (Optional) LLM query handling
├── session_utils.py           # File/session cleanup and tracking
│
├── templates/
│   ├── index.html             # Upload form and query UI
│   ├── answer.html            # Answer display page
│
├── static/
│   └── style.css              # CSS styling for frontend
│
├── requirements.txt
└── README.md
```

---

## 🧪 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/LegalSense.git
cd LegalSense
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI app

```bash
uvicorn main:app --reload
```

### 5. Open in your browser

```
http://localhost:8000
```

---

## 🧹 Session Privacy

- Each user session is assigned a unique ID.
- Uploaded PDFs and vector data are stored temporarily and deleted after the session.
- No data is stored long-term, ensuring privacy and security.

---

## 📄 Example Use Case

Upload a file like `nda_agreement.pdf` and ask:

> "What are the confidentiality clauses?"

LegalSense will:
- Parse and chunk the PDF
- Embed text using LegalBERT
- Search relevant sections
- Return an answer using the source document context

---

## ✅ Future Improvements

- Role-based access control (RBAC)
- Multi-user login
- PDF preview with highlighting
- Save or export chat logs

---
---

## 🙌 Acknowledgments

- [LegalBERT](https://huggingface.co/nlpaueb/legal-bert-base-uncased)
- [ChromaDB](https://www.trychroma.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
