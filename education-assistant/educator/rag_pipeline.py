# educator/rag_pipeline.py
from educator.retriever import retrieve_local, retrieve_wikipedia, retrieve_from_google
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def gather_context(query):
    local = retrieve_local(query)
    wiki = retrieve_wikipedia(query)
    web = retrieve_from_google(query)

    return "\n\n".join([
        "Local Docs:\n" + "\n".join(local),
        "Wikipedia:\n" + wiki,
        "Web Search:\n" + web
    ])

def generate_answer(query, context):
    prompt = f"""You are a helpful assistant trained in Indian legal awareness.

Context:
{context}

Question:
{query}

Answer in simple, educational language:"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def legal_education_rag(query):
    context = gather_context(query)
    return generate_answer(query, context)
