from flask import Flask, request, jsonify, render_template
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import time  # To track the time
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHROMA_PATH = os.getenv('CHROMA_PATH')

# Initialize Flask app
app = Flask(__name__)

# Function to create the QA chain
def create_qa_chain():
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, db.as_retriever(), contextualize_q_prompt
    )

    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

# Load the database and chain at startup
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
qa_chain = create_qa_chain()

# Chat history for the session
chat_history = []

# Route to render the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle questions
@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'answer': 'No question provided'})

    # Measure start time for the retrieval process
    start_time = time.time()

    # Use LangChain QA chain to process the query
    result = qa_chain.invoke({"input": user_question, "chat_history": chat_history})

    # Measure end time and calculate retrieval time
    end_time = time.time()
    retrieval_time = round(end_time - start_time, 2)

    context_documents = result.get('context', [])

    # Combine all page contents and their sources into a single text
    retrieved_context = " ".join([doc.page_content for doc in context_documents])
    context_sources = ", ".join([doc.metadata['source'] for doc in context_documents])

    answer = result["answer"]

    # Append to chat history
    chat_history.extend(
        [
            HumanMessage(content=user_question),
            AIMessage(content=answer),
        ]
    )

    return jsonify({
        'answer': answer,
        'context': retrieved_context,
        'retrieval_time': retrieval_time,
        'source' : context_sources
    })

# API route to clear chat history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    global chat_history
    chat_history = []
    return jsonify({'message': 'Chat history cleared'})

if __name__ == '__main__':
    app.run(debug=True)
