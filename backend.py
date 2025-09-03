from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from core_logic import initialize_rag_chain, query_rag_chain

# Initialize the FastAPI app
app = FastAPI(
    title="HR Resource Query Chatbot API",
    description="An API for querying an HR assistant chatbot powered by a RAG system.",
    version="1.0.0"
)

# Pydantic model for the request body
class ChatQuery(BaseModel):
    query: str

@app.on_event("startup")
def on_startup():
    """
    Event handler for application startup.
    Initializes the RAG chain.
    """
    print("Application starting up...")
    initialize_rag_chain()

@app.get("/", tags=["Health Check"])
def read_root():
    """
    Root endpoint for health check.
    """
    return {"status": "API is running"}

@app.post("/chat", tags=["Chatbot"])
def handle_chat_query(chat_query: ChatQuery):
    """
    Endpoint to handle chat queries.
    It takes a user's natural language query and returns the chatbot's response.
    """
    if not chat_query.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        print(f"Received query: {chat_query.query}")
        # Query the RAG chain from the core logic
        response = query_rag_chain(chat_query.query)
        print(f"Generated response: {response}")
        return {"response": response}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # This block allows you to run the API directly for testing
    uvicorn.run(app, host="0.0.0.0", port=8000)
