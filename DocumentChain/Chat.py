import os
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema import  SystemMessage,HumanMessage,AIMessage
from documentchain import Load_db_from_document as load_db

# Load API key from .env file
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY"

class Chat_with_ai(load_db):
    def __init__(self,query,k):
        super().__init__(folder_path='./DocumentChain/Langchain_testdata/',query='')
        self.db = super().load_folder() # "Langchain_testdata/"
        self.k = k
        self.query = query
        self.messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content="Hi AI, how are you today?"),
            AIMessage(content="I'm great thank you. How can I help you?")
        ]
        self.transcript = self.get
        self.response = self.chat
    
    @property
    def get(self):
        docs =self.db.similarity_search(self.query,k=self.k)
        #print(docs)
        docs_page_content = ' '.join([doc.page_content for doc in docs])
        return docs_page_content
    
    @property
    def chat(self):
        chat = ChatOpenAI(  # intialize chat model
            openai_api_key=os.environ["OPENAI_API_KEY"],
            model='gpt-3.5-turbo'
        )
        self.messages.append(SystemMessage(content=self.transcript))
        self.messages.append(HumanMessage(content=self.query))
        response =chat(self.messages)
        self.messages.append(AIMessage(content=response))
        return response


# get query from main.py

query = 'how to make a good coffee'
chat = Chat_with_ai(query,3)


print(chat.response)



