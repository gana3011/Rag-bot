from rag.vectorstore import vector_store

def embed_text(splits):
    vector_store.add_documents(documents=splits)
