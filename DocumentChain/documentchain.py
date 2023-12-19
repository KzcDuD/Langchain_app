from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv


class Chain():
    def __init__(self,folder_path:str,query:str):
        load_dotenv()
        self.folder = folder_path
        self.query = query
        self.__db = self.__load_folder()
        self.response = self.__get_response_from_query(self.__db,self.query)
        self.response_record = ''
        
    def __load_docx(self,filename:str):
        loader = Docx2txtLoader(filename)
        transcript = loader.load()
        return transcript
    
    def __load_PDF(self,filename:str):
        loader = PyPDFLoader(filename)
        pages = loader.load_and_split()
        return pages
    
    # need to chage:
    # split the docx and pdf file into different folder
    # using dirctory loader to load docx and pdf file in the different folder
    # Response + db keep remember the conversation
    
    def __load_folder(self)->FAISS:
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
    
    def __get_response_from_query(self,db,query,k=4)->str:
        # print(data) # data is a list of Document objects
        # k depaned on the model token length
        docs =db.similarity_search(query,k=k)
        #print(docs)
        docs_page_content = ' '.join([doc.page_content for doc in docs])
        # print(docs_page_content)
        llm = OpenAI(model='text-davinci-003') # https://platform.openai.com/docs/models
        prompt = PromptTemplate(
            input_variables=["question","docs"],
            template="""
                You are a helpful RedHat Rhcsa exam assistant from Taiwan that can answer questions about note based on the notation's transcript .
                
                This is questions and responses record: {response_record}.
                Answer the following question: {question}.
                By searching the following noting transcript: {docs}.
                
                Only use the factual information from the transcript to answer the question.
                If you feel like you don't have enough information in transcript to answer the question, say "I don't know"
                Your answers should be detailed but don't repeat the question ,thank you. (reply in zh-tw)
                """
        )
        chain = LLMChain(llm=llm, prompt=prompt, output_key="response")
        # response records ### AttributeError: 'Chain' object has no attribute 'response_record'
        response = chain.run(response_record = '',question=query,docs=docs_page_content)
        return response
    
    def __str__(self):
        response= self.__get_response_from_query(self.__db,self.query)
        return response

if __name__ == "__main__":
    query = "what is crontab?"
    path= "Langchain_testdata/"
    ch = Chain(path,query)
    print(ch.response)