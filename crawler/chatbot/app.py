from aiohttp import web
from asyncio import to_thread
from .llm import setup_llm, setup_qa_chain
from .retriever import setup_retriever

MAX_PROMPT_CHARS = 2048  # Limit for prompt
MAX_DOC_CHARS = 1500     # Limit for each document chunk

# === Setup LLM and Retriever ===
try:
    retriever = setup_retriever(search_kwargs={"k": 3})  # Return fewer documents
    llm = setup_llm()
    qa_chain = setup_qa_chain(llm, retriever)
    CHAIN_LOADED = True
    CHAIN_ERROR = None
except Exception as e:
    CHAIN_LOADED = False
    CHAIN_ERROR = str(e)

def truncate_text(text: str, max_chars: int) -> str:
    return text[:max_chars]

# === Homepage HTML ===
async def index(request):
    if not CHAIN_LOADED:
        return web.Response(
            text=f"<h1>❌ QA Chain Initialization Failed</h1><p>{CHAIN_ERROR}</p>",
            content_type='text/html',
            status=500
        )
    return web.Response(text="""
        <html>
        <head><title>Code Assistant</title></head>
        <body style="font-family: monospace; background-color: #1e1e1e; color: white; padding: 40px;">
            <h1>💻 Code Assistant</h1>
            <form action="/prompt" method="post">
                <textarea name="prompt" rows="10" cols="80" placeholder="Ask a coding question..."></textarea><br><br>
                <input type="submit" value="Ask">
            </form>
        </body>
        </html>
    """, content_type='text/html')


# === Handle User Prompt ===
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

    truncated_prompt = truncate_text(prompt, MAX_PROMPT_CHARS)
    print(f"[PROMPT RECEIVED] {truncated_prompt}")

    try:
        # Safely call the chain using invoke()
        result = await to_thread(qa_chain.invoke, {"query": truncated_prompt})
        answer = result.get("result", "No answer.")
        sources = result.get("source_documents", [])

        sources_html = "".join(
            f"<li><strong>ID:</strong> {doc.metadata.get('id', 'N/A')}<br>"
            f"<em>{truncate_text(doc.page_content, MAX_DOC_CHARS)}...</em></li>"
            for doc in sources
        )

        response_html = f"""
        <html>
        <head><title>Code Answer</title></head>
        <body style="font-family: monospace; background-color: #1e1e1e; color: white; padding: 40px;">
            <h2>🧠 Answer</h2>
            <pre style="background-color:#2e2e2e; padding: 15px; border-radius: 8px;">{answer}</pre>
            <h3>📚 Sources</h3>
            <ul>{sources_html}</ul>
            <p><a href="/" style="color: #4d90fe;">← Back</a></p>
        </body>
        </html>
        """
        return web.Response(text=response_html, content_type='text/html')

    except Exception as e:
        print(f"[ERROR] Chain execution failed: {e}")
        return web.Response(
            text=f"<h1>Error:</h1><p>{str(e)}</p>",
            status=500,
            content_type='text/html'
        )


# === App Setup ===
app = web.Application()
app.add_routes([
    web.get('/', index),
    web.post('/prompt', handle_prompt),
])

if __name__ == '__main__':
    print("🚀 Starting Code Assistant at http://localhost:8080")
    if not CHAIN_LOADED:
        print(f"⚠️ Chain load failed: {CHAIN_ERROR}")
    web.run_app(app, host='0.0.0.0', port=8080)
