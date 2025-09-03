# HR Resource Query Chatbot

## Overview
This project is an intelligent HR assistant chatbot designed to help HR teams and project managers quickly find suitable employees based on natural language queries. The application leverages a Retrieval-Augmented Generation (RAG) architecture, allowing it to understand user requests and provide contextually-aware recommendations from a structured employee dataset.

The core approach involves converting employee profiles from a JSON file into vector embeddings, storing them in a searchable index, and using a Large Language Model (LLM) to generate natural language responses based on the most relevant retrieved candidates.

## Features
Natural Language Querying: Users can ask complex questions like "Find Python developers with 3+ years of experience" or "Who has worked on healthcare projects?".

RAG-Powered Responses: Provides accurate, context-aware answers grounded in the provided employee data, minimizing AI hallucinations.

Structured Data Handling: Efficiently processes a JSON dataset of employee profiles, making the system easily extensible.

RESTful API: A robust FastAPI backend that exposes a simple /chat endpoint for the AI logic.

Interactive UI: A clean and user-friendly chat interface built with Streamlit.

Scalable Architecture: Decoupled frontend and backend services allow for independent scaling and development.

## Architecture
The system is designed with a modern, decoupled architecture consisting of a frontend UI, a backend API, and a core AI logic component.

Frontend (Streamlit): A simple web interface where the user inputs their query. It sends an HTTP POST request to the FastAPI backend.

Backend (FastAPI): A Python-based API server that handles incoming requests. It contains the main business logic and orchestrates the RAG process.

Core AI Logic (LangChain): The heart of the application, which executes the RAG pipeline:

Data Loading: At startup, employee data from data.json is loaded and transformed into LangChain Document objects.

Embedding: Each document (employee profile) is converted into a numerical vector using a sentence-transformers model from Hugging Face.

Vector Store (FAISS): The embeddings are stored in a FAISS index, which allows for rapid semantic similarity searches.

Retrieval: When a query is received, a MultiQueryRetriever generates variations of the query to find the most relevant employee documents from the FAISS index.

Generation: The retrieved documents are passed as context along with the original query to the Google Gemini LLM, which generates a final, human-readable response.

## Setup & Installation
Follow these steps to run the project on your local machine.

Prerequisites
Python 3.9+

A Google Gemini API Key.

1. Clone the Repository & Install Dependencies
It is highly recommended to use a virtual environment.

# Clone or create your project folder
# cd your-project-folder

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt

2. Set Up Environment Variables
Create a file named .env in the root directory of the project and add your Google Gemini API key:

GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

3. Run the Application
You must run the backend and frontend in two separate terminals.

Terminal 1: Start the Backend (FastAPI)

uvicorn backend:app --reload

The server will be available at http://127.0.0.1:8000. Wait for the log to show "Application startup complete."

Terminal 2: Start the Frontend (Streamlit)

streamlit run frontend.py

The chat interface will open in your browser, typically at http://localhost:8501.

## API Documentation
The backend exposes a single primary endpoint for chat interactions.

POST /chat
This endpoint processes a user's natural language query and returns the AI-generated response.

Request Body:

{
  "query": "Find developers who know both AWS and Docker"
}

Success Response (200 OK):

{
  "response": "Based on your query, I found Peter Hall. He has 4 years of experience with skills in Python, AWS, and Docker. He has worked on projects like 'Log Anomaly Detection' and 'Cloud Deployment Automation' and is currently available."
}

Example curl Request:

curl -X POST "[http://127.0.0.1:8000/chat](http://127.0.0.1:8000/chat)" \
-H "Content-Type: application/json" \
-d '{"query": "Find developers who know both AWS and Docker"}'

Of course. Here are the detailed answers for each of those sections, based on the project we built together.

## AI Development Process
Document how you used AI tools in your development:

Which AI coding assistants did you use?

This project was developed  with help of ChatGPT  as well as Gemini as the AI  assistant.

How did AI help in different phases?

Architecture & Code Generation: The AI assistant was pivotal in structuring the entire application. It took the initial requirement of an "HR Chatbot" and proposed the decoupled FastAPI backend and Streamlit frontend architecture.

Debugging: This was one of the most critical contributions. The AI diagnosed two major blockers by analyzing terminal logs and screenshots:

Connection Error: It identified that the frontend couldn't connect to the backend and correctly deduced that the backend server wasn't running.

API Key Error: It parsed the Python traceback to pinpoint the missing GEMINI_API_KEY and provided the exact steps to create a .env file to resolve it.

Documentation & Testing: The AI generated a comprehensive README.md file and provided lists of specific, targeted questions to test the chatbot's functionality against the provided employee data.

What percentage of code was AI-assisted vs hand-written?

Approximately 90% of the code was AI-generated. The remaining 10% involved manual tasks like creating the .env file, typing the commands into the terminal, and providing the initial project requirements and follow-up prompts to the AI.

Any interesting AI-generated solutions or optimizations?

Yes, the use of MultiQueryRetriever from LangChain was an AI-suggested optimization. Instead of just using a basic retriever, the AI implemented this more advanced technique which uses the LLM to generate multiple variations of a user's question. This leads to a more robust search and ensures that more relevant employee profiles are found and passed to the final generation step.

Challenges where AI couldn't help and you solved manually?

The primary challenge was the AI's inability to interact with the local development environment. All physical tasks had to be performed manually based on the AI's instructions. This included:

Creating the project folder and file structure.

Setting up the Python virtual environment.

Installing all dependencies using pip.

Creating the .env file and pasting in the secret API key.

Running the backend and frontend servers in separate terminals.

## Technical Decisions
Explain your choice of technologies and trade-offs:

Why did you choose Google Gemini (Cloud API) vs open-source models?

We chose the Google Gemini API primarily for its combination of high performance and ease of use. For a project like this, it allows for rapid development without the overhead of managing local infrastructure. It provides access to a state-of-the-art model with a simple API call, which is ideal for prototyping and building quickly.

Local LLM (Ollama) vs cloud API considerations?

This choice represents a fundamental trade-off in AI application development:

Cloud API (Chosen):

Pros: Easy setup, no need for powerful local hardware (GPU), access to the most powerful models, managed infrastructure.

Cons: Incurs costs per API call, requires an internet connection, and involves sending data to a third-party service (potential privacy concerns).

Local LLM (e.g., using Ollama):

Pros: Complete data privacy and security (data never leaves your machine), no per-call costs, works offline.

Cons: Requires a powerful local machine (often with a high-VRAM GPU), more complex to set up and maintain, and the performance of local models may not match the top-tier cloud models.

Performance vs cost vs privacy trade-offs?

The architecture of this project prioritizes development speed and performance over strict privacy and operational cost. By using a managed cloud API, we could focus on the application logic rather than model hosting. This is a common and effective strategy for building proofs-of-concept and internal tools. For a production system handling sensitive HR data, the trade-off would likely shift, making a locally-hosted LLM a more suitable choice despite the higher initial setup effort.

## Future Improvements
What would you add with more time?

Database Integration: Replace the static data.json file with a scalable database like PostgreSQL or a NoSQL option like MongoDB. This would allow HR to add, update, and remove employees through a dedicated interface without needing to edit a text file.

Enhanced Frontend UI: Display search results in structured UI cards instead of a single block of text. Each card could represent an employee and cleanly display their photo, skills, experience, and a link to their full profile.

Authentication & Authorization: Implement a login system (e.g., using OAuth or JWT) to ensure that only authorized HR personnel and managers can access the chatbot and employee data.

Conversational Memory: Add a memory component to the RAG chain so the chatbot can remember the context of the current conversation. This would allow for follow-up questions like "Of those two, who has worked on mobile apps?".

Feedback Mechanism: Include a simple "thumbs up/thumbs down" button on each response. This feedback could be logged and used to fine-tune the retrieval model or the LLM prompts to improve accuracy over time.

Containerization and Deployment: Package the backend and frontend into Docker containers and write a docker-compose file. This would standardize the deployment process and make it easy to host the application on a cloud platform like AWS, Google Cloud, or Heroku.

## Demo
image :
![alt text](<WhatsApp Image 2025-09-04 at 00.52.59_0f204c40.jpg>)


