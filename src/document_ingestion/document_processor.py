"""Document Ingestion module for processing PDFs and text files"""

from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_documents(self, src: str) -> List[Document]:
        docs = []
        path = Path(src)
        if path.is_dir():
            docs.extend(self.load_from_pdf_dir(path))
        elif path.suffix.lower() == ".pdf":
            docs.extend(self.load_from_pdf(path))
        elif path.suffix.lower() == ".txt":
            docs.extend(self.load_from_txt(path))
        return docs

    def load_from_pdf_dir(self, dir_path: Path) -> List[Document]:
        docs = []
        for file in dir_path.glob("*.pdf"):
            docs.extend(self.load_from_pdf(file))
        return docs

    def load_from_pdf(self, file_path: Path) -> List[Document]:
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(str(file_path))
        return loader.load()

    def load_from_txt(self, file_path: Path) -> List[Document]:
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(str(file_path), encoding="utf-8")
        return loader.load()

    def split_documents(self, docs: List[Document]) -> List[Document]:
        return self.splitter.split_documents(docs)
