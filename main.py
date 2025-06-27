from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uuid

from pdf_utils import parse_and_chunk_pdf
from embedding_utils import load_legalbert, embed_chunks
from vectorstore_utils import store_embeddings, query_chromadb, cleanup_collection
from session_utils import save_pdf, delete_pdf
from llm_utils import get_llm_answer

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load model/tokenizer once
tokenizer, model = load_legalbert()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
def upload_pdf(request: Request, file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    file_path = save_pdf(file, session_id)
    chunks = parse_and_chunk_pdf(file_path)
    embeddings = embed_chunks(chunks, tokenizer, model)
    store_embeddings(session_id, chunks, embeddings)
    response = RedirectResponse(url=f"/ask?session_id={session_id}", status_code=303)
    return response

@app.get("/ask", response_class=HTMLResponse)
def ask_page(request: Request, session_id: str):
    return templates.TemplateResponse("ask.html", {"request": request, "session_id": session_id, "answer": None})

@app.post("/ask", response_class=HTMLResponse)
def ask_question(request: Request, session_id: str = Form(...), question: str = Form(...)):
    # Embed the question
    inputs = tokenizer([question], padding=True, truncation=True, return_tensors="pt", max_length=512)
    outputs = model(**inputs)
    q_embedding = outputs.last_hidden_state[:, 0, :].cpu().detach().numpy()
    relevant_chunks = query_chromadb(session_id, q_embedding)
    if relevant_chunks:
        context = "\n".join(relevant_chunks)
        try:
            answer = get_llm_answer(question, context)
        except Exception as e:
            answer = f"[LLM Error: {e}]"
    else:
        answer = "No relevant information found."
    return templates.TemplateResponse("ask.html", {"request": request, "session_id": session_id, "answer": answer})

@app.post("/cleanup")
def cleanup(session_id: str = Form(...)):
    delete_pdf(session_id)
    cleanup_collection(session_id)
    return {"status": "cleaned up"} 