import os
from dotenv import load_dotenv

load_dotenv()

def retrieve_ans(query, vector_store, llm, k):
    retrieved_docs = vector_store.similarity_search(query, k=k)

    context = "\n\n".join(
        f"[Page {doc.metadata.get('page_number')}]\n{doc.page_content}"
        for doc in retrieved_docs
    )

    prompt = f"""
You are an assistant answering questions based ONLY on the context retrieved from document given below.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""
    
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": [doc.metadata for doc in retrieved_docs]
    }