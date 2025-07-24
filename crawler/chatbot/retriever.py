from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from .db_utilits import load_pages_as_documents


def setup_retriever():
    docs = load_pages_as_documents()
    if not docs:
        raise ValueError("No documents found in the database to build the retriever.")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})
