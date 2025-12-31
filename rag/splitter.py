from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedder import embed_text

def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 150,
        separators=["\n\n", "\n", " ", ""]
    )

    splits = splitter.split_documents(documents)

    embed_text(splits)