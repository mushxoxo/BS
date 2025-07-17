from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from scraper import scrape_articles
from vector import refresh_vector_store
import App

model = OllamaLLM(model="llama3.2")

template = """
You are an assistant that provides summaries or answers using recent business news articles.

QUESTION:
{question}

USE THE FOLLOWING INFORMATION TO ANSWER:
{info}

Only use the provided information to answer. If the answer is not present, say "I couldn't find any relevant information."

Your answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------------")
    question = App.query.strip()

    if question.lower() == "q":
        break

    print("\n[Step 1] Scraping articles...")
    scrape_articles(question)

    print("[Step 2] Refreshing vector store...")
    retriever = refresh_vector_store()

    print("[Step 3] Retrieving relevant content...")
    retrieved_docs = retriever.invoke(question)

    if not retrieved_docs:
        print("No relevant articles found.")
        continue

    info = ""
    for i, doc in enumerate(retrieved_docs):
        print(f"\n--- Retrieved Doc #{i+1} ---")
        print("Metadata:", doc.metadata)
        info += doc.page_content + "\n\n"

    print("[Step 4] Asking LLM...\n")
    result = chain.invoke({"info": info, "question": question})

    print("\n\nAnswer:\n", result)
