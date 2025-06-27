import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_pdf(file, session_id):
    file_path = os.path.join(UPLOAD_DIR, f"{session_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def delete_pdf(session_id):
    file_path = os.path.join(UPLOAD_DIR, f"{session_id}.pdf")
    if os.path.exists(file_path):
        os.remove(file_path) 