from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

class Load_db_from_document:
    def __init__(self,folder_path:str,query:str):
        load_dotenv()
        self.folder = folder_path
        self.query = query
        self.db = self.load_folder()
        
    def __load_docx(self,filename:str):
        loader = Docx2txtLoader(filename)
        transcript = loader.load()
        return transcript
    
    def __load_PDF(self,filename:str):
        loader = PyPDFLoader(filename)
        pages = loader.load_and_split()
        return pages
    
    def load_folder(self)->FAISS:
        embeding = OpenAIEmbeddings()
        files = os.listdir(self.folder)
        if files[0].endswith(".docx"):
            transcript= self.__load_docx(self.folder+files[0])
        elif files[0].endswith(".pdf"):
            transcript= self.__load_PDF(self.folder+files[0])
        for file in files[1:]:
            if file.endswith(".docx"):
                data = self.__load_docx(self.folder+file)
                transcript+=data
            elif file.endswith(".pdf"):
                data = self.__load_PDF(self.folder+file)
                transcript+=data
    
        text_spilter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap=100)
        docs = text_spilter.split_documents(transcript)
        db = FAISS.from_documents(docs ,embeding)
        return db
    