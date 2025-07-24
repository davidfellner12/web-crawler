from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

CUSTOM_RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful coding assistant. Use the following information retrieved from a documentation database, along with your own knowledge, to answer the user's question in a helpful and complete way.

Context:
{context}

Question:
{question}

Answer:"""
)

def setup_llm():
    pipe = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        max_length=512,
        do_sample=True,
        top_p=0.95,
        temperature=0.7,
    )
    return HuggingFacePipeline(pipeline=pipe)

def setup_qa_chain(llm, retriever):
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": CUSTOM_RAG_PROMPT}
    )
