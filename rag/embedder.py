import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

load_dotenv()

def embed_text(splits):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", api_key=os.getenv("GEMINI_API_KEY"))
    
    client = QdrantClient(host="localhost", port=6333,)

    #finding the vector size of collection
    vector_size = len(embeddings.embed_query("sample text"))

    if not client.collection_exists("ragbot"):
        client.create_collection(
            collection_name="ragbot",
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="ragbot",
        embedding=embeddings,
    )

    ids = vector_store.add_documents(documents=splits)
    print(ids)

