from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv

load_dotenv()

def Load_Document(filename:str):
    loader = Docx2txtLoader(filename)
    transcript = loader.load()
    return transcript
    
def get_response_from_query(db,query,k=4):
    # print(data) # data is a list of Document objects
    docs =db.similarity_search(query,k=k)
    #print(docs)
    docs_page_content = ' '.join([doc.page_content for doc in docs])
    # print(docs_page_content)
    llm = OpenAI(model='text-davinci-003')
    prompt = PromptTemplate(
        input_variables=["question","docs"],
        template="""
            please translate the answer to zh-tw:
            You are a helpful RedHat Rhcsa exam assistant from Taiwan that can answer questions about note based on the notation's transcript .
            
            Answer the following question: {question}
            By searching the following noting transcript: {docs}
            
            Only use the factual information from the transcript to answer the question.
            If you feel like you don't have enough information in transcript to answer the question, say "I don't know"
            Your answers should be detailed ,thank you.
            """
    )
    chain = LLMChain(llm=llm, prompt=prompt, output_key="response")
    response = chain.run(question=query,docs=docs_page_content)
    response = response.replace("\n","")
    return response ,docs

def load_folder(path)->FAISS:
    embedings = OpenAIEmbeddings()
    files = os.listdir(path)
    transcript=Load_Document(path+files[0])
    for file in files[1:]:
        if file.endswith(".docx"):
            data = Load_Document(path+file)
            transcript+=data
    
    text_spilter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap=100)
    docs = text_spilter.split_documents(transcript)
    db = FAISS.from_documents(docs ,embedings)
    return db

if __name__ == "__main__":
    query = "what is crontab?"
    db=load_folder("Langchain_testdata/")
    response,docs = get_response_from_query(db,query)
    print(response)