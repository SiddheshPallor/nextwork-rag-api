from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import ollama

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")
ollama_client = ollama.Client(host="http://127.0.0.1:11434")
#ollama_client = ollama.Client(host="http://host.docker.internal:11434")


@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)

    docs = results.get("documents", [])
    context = docs[0][0] if docs and docs[0] else "No relevant context found."

    answer = ollama_client.generate(
    model="tinyllama",
    prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
)


    return {"answer": answer["response"]}

class Document(BaseModel):
    id: str
    text: str

@app.post("/add")
def add_document(doc: Document):
    collection.add(
        documents=[doc.text],
        ids=[doc.id]
    )
    return {"message": "Document added to knowledge base"}

