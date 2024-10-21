from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()
DATA_SRC = os.getenv('DATA_SRC')
CHROMA_PATH = os.getenv('CHROMA_PATH')



#Function to loads PDF documents, splits them into chunks, and creates a vector database.
def create_vector_db(folder_path):

    loaders = [PyPDFLoader(os.path.join(folder_path, fn)) for fn in os.listdir(folder_path)]
    documents = []
    for loader in tqdm(loaders):
        documents.extend(loader.load())

    print("Documents Extacted Successfully")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    print("Chunks Created Successfully")

    print("Creating Embeddings ......")

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_PATH)
    db.persist()
    return db


if __name__ == "__main__":
    db = create_vector_db(DATA_SRC)
    print("Vector Store Created")
