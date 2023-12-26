from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from LoadDocument.load import Load_db_from_document

from dotenv import load_dotenv

class Document_search(Load_db_from_document):
    def __init__(self,folder_path:str,query:str):
        super().__init__(folder_path=folder_path,query=query)
        load_dotenv()
        self.folder = folder_path
        self.query = query
        self.__db = super().load_folder()
        self.response = self.__get_response_from_query(self.__db,self.query)
        self.response_record = ''
        
    
    def __get_response_from_query(self,db,query,k=3)->str:
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
    query = "113年度專題分組黃駿賢表格"
    path= "Langchain_testdata/"
    ch = Document_search(path,query)
    print(ch.response)