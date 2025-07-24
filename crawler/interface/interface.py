import os
import sqlite3
from aiohttp import web
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), 'db', 'pages.db')


def load_pages_as_documents(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at path: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description FROM pages WHERE description IS NOT NULL AND description != ''")
    rows = cursor.fetchall()
    conn.close()

    return [
        Document(page_content=f"{title}\n\n{description}", metadata={"id": pid})
        for pid, title, description in rows
    ]


def setup_retriever():
    docs = load_pages_as_documents(DB_PATH)
    if not docs:
        raise ValueError("No documents found in the database to build the retriever.")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})


def setup_llm():
    pipe = pipeline(
        "text-generation",
        model="google/flan-t5-small",
        max_length=512,
        do_sample=True,
        top_p=0.95,
        temperature=0.7,
    )
    return HuggingFacePipeline(pipeline=pipe)


try:
    retriever = setup_retriever()
    llm = setup_llm()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff"
    )
    CHAIN_LOADED = True
    CHAIN_ERROR = None
except Exception as e:
    CHAIN_LOADED = False
    CHAIN_ERROR = str(e)


async def index(request):
    if not CHAIN_LOADED:
        return web.Response(
            text=f"<h1>❌ QA Chain Initialization Failed</h1><p>{CHAIN_ERROR}</p>",
            content_type='text/html',
            status=500
        )

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Coding Agent</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                height: 100vh;
                background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c1c1c);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }

            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            h1 {
                color: #66ccff;
                text-shadow: 0 0 10px rgba(102, 204, 255, 0.8);
                animation: fadeIn 1.2s ease-in-out;
            }

            form {
                display: flex;
                flex-direction: column;
                align-items: center;
                background-color: rgba(30, 30, 30, 0.9);
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(77,144,254,0.4);
                backdrop-filter: blur(10px);
                animation: fadeInUp 1s ease-out;
            }

            textarea {
                background-color: #2e2e2e;
                color: #ffffff;
                border: 1px solid #4d90fe;
                border-radius: 8px;
                padding: 12px;
                width: 500px;
                height: 200px;
                resize: none;
                font-size: 16px;
                transition: box-shadow 0.3s;
            }

            textarea:focus {
                box-shadow: 0 0 10px rgba(77, 144, 254, 0.6);
                outline: none;
            }

            input[type="submit"] {
                background-color: #4d90fe;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                margin-top: 15px;
                cursor: pointer;
                font-size: 16px;
                box-shadow: 0 4px 10px rgba(77, 144, 254, 0.3);
                transition: background-color 0.3s ease;
            }   

            input[type="submit"]:hover {
                background-color: #3a7fe0;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <h1>🚀 Coding Agent</h1>
        <form action="/prompt" method="post">
            <textarea name="prompt" placeholder="Describe your coding task..."></textarea>
            <br>
            <input type="submit" value="Generate Code">
        </form>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')


async def handle_prompt(request):
    if not CHAIN_LOADED:
        return web.Response(
            text=f"<h1>❌ QA Chain Initialization Failed</h1><p>{CHAIN_ERROR}</p>",
            content_type='text/html',
            status=500
        )

    data = await request.post()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return web.Response(text="No prompt provided.", status=400)

    try:
        result = qa_chain(prompt)
        answer = result["result"]
        sources = result["source_documents"]

        sources_html = "".join(
            f"<li><strong>ID:</strong> {doc.metadata['id']}<br><em>{doc.page_content[:200]}...</em></li>"
            for doc in sources
        )

        response_html = f"""
        <html>
        <head>
            <title>Generated Response</title>
            <style>
                body {{
                    background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1c1c1c);
                    background-size: 400% 400%;
                    animation: gradientBG 15s ease infinite;
                    color: #ffffff;
                    font-family: 'Segoe UI', sans-serif;
                    padding: 30px;
                }}

                @keyframes gradientBG {{
                    0% {{ background-position: 0% 50%; }}
                    50% {{ background-position: 100% 50%; }}
                    100% {{ background-position: 0% 50%; }}
                }}

                .container {{
                    max-width: 800px;
                    margin: auto;
                    background-color: rgba(30, 30, 30, 0.95);
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 0 20px rgba(77,144,254,0.4);
                    backdrop-filter: blur(10px);
                    animation: fadeInUp 0.6s ease-out;
                }}

                pre {{
                    background-color: #2e2e2e;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    white-space: pre-wrap;
                }}

                ul {{
                    list-style-type: none;
                    padding-left: 0;
                }}

                li {{
                    margin-bottom: 15px;
                    background-color: #1e1e1e;
                    padding: 10px;
                    border-left: 3px solid #4d90fe;
                }}

                a {{
                    color: #4d90fe;
                    text-decoration: none;
                }}

                a:hover {{
                    text-decoration: underline;
                }}

                .back {{
                    margin-top: 20px;
                }}

                @keyframes fadeInUp {{
                    from {{ opacity: 0; transform: translateY(30px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🧠 Generated Code</h2>
                <pre>{answer}</pre>
                <h3>🔍 Relevant Sources</h3>
                <ul>{sources_html}</ul>
                <div class="back"><a href="/">← Back to form</a></div>
            </div>
        </body>
        </html>
        """
        return web.Response(text=response_html, content_type='text/html')

    except Exception as e:
        return web.Response(text=f"<h1>Error:</h1><p>{str(e)}</p>", status=500, content_type='text/html')


app = web.Application()
app.add_routes([
    web.get('/', index),
    web.post('/prompt', handle_prompt),
])

if __name__ == '__main__':
    print("🚀 Starting server at http://localhost:8080")
    print(f"📦 Using database: {DB_PATH}")
    if not CHAIN_LOADED:
        print(f"⚠️  Chain load failed: {CHAIN_ERROR}")
    web.run_app(app, host='0.0.0.0', port=8080)
