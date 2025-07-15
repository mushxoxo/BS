from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

def refresh_vector_store():
    df = pd.read_json("articles.jsonl", lines=True)

    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    db_location = "./chrome_langchain_db"

    documents = []
    ids = []

    for i, row in df.iterrows():
        document = Document(
            page_content=f"""
                Title: {row['title']}
                Date: {row['date']} {row['time']}
                Author: {row['author']}
                Category: {row['category']}
                TL;DR: {row['tldr']}
                Content: {row['content']}
            """,
            metadata={"date": str(row["datetime"])},
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

    vector_store = Chroma(
        collection_name="articles",
        persist_directory=db_location,
        embedding_function=embeddings
    )

    vector_store.add_documents(documents=documents, ids=ids)
    return vector_store.as_retriever(search_kwargs={"k": 10})
