"""Vector Store wrapper using FAISS and embeddings"""

import os
from langchain_community.vectorstores import FAISS
from src.config.config import Config

class VectorStore:
    def __init__(self, persist_dir: str = "faiss_index"):
        self.persist_dir = persist_dir
        
        # Resolve embeddings dynamically based on active model config
        if Config.USE_GEMINI:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            api_key = Config.get_gemini_key()
            os.environ["GOOGLE_API_KEY"] = api_key
            self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        else:
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings()
            
        self.db = None

    def create_vectorstore(self, chunks):
        self.db = FAISS.from_documents(chunks, self.embeddings)
        self.save_local(self.persist_dir)

    def get_retriever(self):
        if self.db is None:
            if os.path.exists(self.persist_dir):
                self.load_local(self.persist_dir)
            else:
                raise ValueError("Vector store not initialized and no saved index found.")
        return self.db.as_retriever()

    def save_local(self, path: str):
        if self.db is not None:
            self.db.save_local(path)

    def load_local(self, path: str):
        self.db = FAISS.load_local(path, self.embeddings, allow_dangerous_deserialization=True)
