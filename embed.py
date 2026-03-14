import chromadb
import os

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

docs_folder = "docs"

for file in os.listdir(docs_folder):
    if file.endswith(".txt"):

        with open(f"{docs_folder}/{file}", "r") as f:
            text = f.read()

        collection.add(
            documents=[text],
            ids=[file]
        )

        print(file + " embedded")

print("Embedding stored in Chroma")