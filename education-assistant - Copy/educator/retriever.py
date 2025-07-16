# educator/retriever.py
import wikipedia
import json
import faiss  # spell-checker: disable-line
from sentence_transformers import SentenceTransformer
import requests
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/education_docs.json") as f:
    docs = json.load(f)

texts = [doc["content"] for doc in docs]
vectors = model.encode(texts)
index = faiss.IndexFlatL2(len(vectors[0]))
index.add(vectors)

def retrieve_local(query, k=3):
    q_vec = model.encode([query])
    _, I = index.search(q_vec, k)
    return [texts[i] for i in I[0]]

def retrieve_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except Exception as e:
        return f"(Wikipedia Error: {e})"

def retrieve_from_google(query):
    try:
        headers = {"X-API-KEY": os.getenv("SERPER_API_KEY")}
        params = {"q": query}
        resp = requests.get("https://google.serper.dev/search", headers=headers, params=params)
        results = resp.json().get("organic", [])
        return "\n".join([r["snippet"] for r in results[:3]])
    except Exception as e:
        return f"(Google Search Error: {e})"
