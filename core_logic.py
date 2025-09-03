import os
import json
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the System Prompt for the HR Assistant
SYSTEM_PROMPT = """
You are an expert HR assistant. Your purpose is to find the best-suited employees for a query based on the provided employee profiles.
When a user asks you to find employees, analyze their skills, experience, and project history.

Guidelines:
- Present the most relevant candidates first.
- For each recommended candidate, provide a concise summary including their name, years of experience, key skills relevant to the query, and relevant past projects.
- If multiple candidates are suitable, list them out clearly.
- If no suitable candidates are found in the provided documents, state that clearly. Do not make up information.
- Your tone should be professional, helpful, and efficient.

Example Response:
"Based on your request for a Python developer with AWS experience, I found two excellent candidates:

1.  **Alice Johnson**: With 5 years of experience, Alice is a strong fit. Her skills include Python and AWS, and she has worked on a 'Healthcare Dashboard' which could be relevant. She is currently available.
2.  **Emily Rodriguez**: Emily has 7 years of experience in cloud infrastructure, specializing in AWS and Python. Her work on 'Cloud Infrastructure Automation' makes her another great choice. She is also available."
"""

# Global variable to hold the initialized RAG chain to avoid re-initialization on every API call
rag_chain = None

def initialize_rag_chain():
    """
    Initializes the RAG chain by loading data, creating retrievers,
    and setting up the LLM. This should be called once on application startup.
    """
    global rag_chain

    if rag_chain is not None:
        print("RAG chain is already initialized.")
        return rag_chain

    print("Initializing RAG chain...")

    # 1. Load and Process Employee Data
    docs = load_employees_as_documents('data.json')

    # 2. Create Embeddings and Vector Store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/msmarco-distilbert-base-v4")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 3. Initialize LLM
    llm = initialize_llm()

    # 4. Create Multi-Query Retriever
    multi_query_retriever = MultiQueryRetriever.from_llm(
        retriever=vectorstore.as_retriever(),
        llm=llm
    )

    # 5. Set up the RAG pipeline
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=multi_query_retriever,
        return_source_documents=False # We don't need to return the full source documents to the user
    )

    print("RAG chain initialization complete.")
    return rag_chain

def load_employees_as_documents(file_path):
    """
    Loads employee data from a JSON file and converts each employee into a
    LangChain Document object for processing.
    """
    all_documents = []
    with open(file_path, 'r') as f:
        data = json.load(f)

    for employee in data['employees']:
        # Create a comprehensive text string for the document content
        content = (
            f"Name: {employee['name']}. "
            f"Experience: {employee['experience_years']} years. "
            f"Skills: {', '.join(employee['skills'])}. "
            f"Past Projects: {', '.join(employee['projects'])}. "
            f"Availability: {employee['availability']}."
        )
        
        # The metadata can be useful for filtering or direct lookups if needed later
        metadata = {"id": employee['id'], "name": employee['name']}

        # Create a Document object
        doc = Document(page_content=content, metadata=metadata)
        all_documents.append(doc)

    print(f"Loaded and processed {len(all_documents)} employee profiles.")
    return all_documents


def initialize_llm():
    """Initializes the Google Gemini LLM with a custom system prompt."""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

    return GoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=gemini_api_key,
        system_message=SYSTEM_PROMPT,
        temperature=0.2 # Lower temperature for more deterministic, factual responses
    )

def query_rag_chain(question: str):
    """
    Queries the initialized RAG chain.
    """
    global rag_chain
    if rag_chain is None:
        raise RuntimeError("RAG chain is not initialized. Call initialize_rag_chain() first.")
    
    response = rag_chain.invoke(question)
    return response.get("result", "Sorry, I encountered an error.")
