from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from retriever import load_vector_store

def get_chatbot():
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_type="similarity", k=3)

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

if __name__ == "__main__":
    chatbot = get_chatbot()
    while True:
        query = input("Your question: ")
        response = chatbot(query)
        print("Answer:", response["result"])
        print("Sources:", [doc.metadata['source'] for doc in response["source_documents"]])
