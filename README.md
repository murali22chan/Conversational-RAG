# Conversational RAG with Chat Memory 
This project is a Conversational Question-Answering (QA) system built using Flask for the backend, LangChain for retrieval-based QA, and Bootstrap for a clean frontend interface. The system utilizes a custom retriever with context-aware question formulation and returns responses based on a provided knowledge base.
## Features
1) Conversational QA with context-aware question reformulation.
2) Fast and accurate retrieval of relevant information.
3) Display the retrieved context and response time on the front end.
4) Clear chat history functionality.
5) API-based backend with a dynamic Bootstrap-powered frontend.

## Technologies Used

Flask: Backend web framework.
LangChain: Language chain and retrieval model for context-aware Q&A.
SentenceTransformerEmbeddings: Embeddings for document retrieval.
Chroma: Vectorstore for storing document embeddings.
Bootstrap: For a simple and responsive frontend design.
OpenAI API: Language model used to generate responses.
JavaScript: To handle frontend interactions.

## Usage

1. Git Clone the Repo
```python
git clone https://github.com/murali22chan/Conversational-RAG.git
```
2. Install the required packages. (pip3 for python 3.8.X >)
```python 
pip install -r requirements.txt 
```
3. Environment Variables: Create a .env file and set the following variables
```python 
OPENAI_API_KEY=<your_openai_api_key>
CHROMA_PATH=<path_to_chroma_db>
```
4. Run the Flask app
```python 
python run app.py
```
5. Visit http://127.0.0.1:5000 to interact with the chat interface.
