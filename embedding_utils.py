from transformers import AutoTokenizer, AutoModel
import torch

LEGAL_BERT_MODEL = "nlpaueb/legal-bert-base-uncased"

def load_legalbert():
    tokenizer = AutoTokenizer.from_pretrained(LEGAL_BERT_MODEL)
    model = AutoModel.from_pretrained(LEGAL_BERT_MODEL)
    return tokenizer, model

@torch.no_grad()
def embed_chunks(chunks, tokenizer, model):
    inputs = tokenizer(chunks, padding=True, truncation=True, return_tensors="pt", max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
    return embeddings 