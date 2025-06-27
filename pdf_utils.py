import fitz  # PyMuPDF

def parse_and_chunk_pdf(pdf_path, chunk_size=300):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks 