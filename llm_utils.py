import google.generativeai as genai
import os

def get_llm_answer(question, context, api_key=None):
    """
    Calls Gemini LLM with the user's question and context (retrieved chunks).
    Returns the generated answer as a string.
    """
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
        # api_key = ""
    if not api_key:
        raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY env variable or pass as argument.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = (
        "You are a legal assistant. Use the following context from a legal document to answer the user's question.\n"
        f"Context:\n{context}\n"
        f"Question: {question}\n"
        "Answer:"
    )
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, 'text') else str(response)
