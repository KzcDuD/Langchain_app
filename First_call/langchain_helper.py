from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
#
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
#
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
#
from dotenv import load_dotenv

load_dotenv()

# basic
def generate_pet_name(animal_type,pet_color):
    llm =OpenAI(temperature =0.7) # The model creative temperature
    prompt_template_name = PromptTemplate(
        input_variables =['animal_type'],
        template="I have a {animal_type} pet and I want a coll name for it , it is {pet_color} in color. Suggest me five cool names for my pet."
    )
    name_chain = LLMChain(llm=llm,prompt=prompt_template_name , output_key='pet_name')
    response =  name_chain({'animal_type':animal_type,'pet_color':pet_color})
    
    return response

# Agent wikipedia
def langchain_agent():
    llm =OpenAI(temperature =0.7) # The model creative temperature
    tools = load_tools(["wikipedia","llm-math"],llm=llm)
    agent = initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION , verbose=True)
    result = agent.run("What is the average age of a dog? Multiple the age by 3")
    print(result)


embedings = OpenAIEmbeddings()
# Youtube transfer
def create_vector_db_from_youtube(youtube_url:str)->FAISS:
    loader = YoutubeLoader.from_youtube_url(youtube_url)
    transcript= loader.load()
    # print(transcript)
    
    text_spilter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap=100)
    docs = text_spilter.split_documents(transcript)
    db = FAISS.from_documents(docs ,embedings)
    return db
    
def get_response_from_query(db,query,k=4):
    # text-davinci can handle 4079 tokens
    docs =db.similarity_search(query,k=k)
    #print(docs)
    docs_page_content = ' '.join([doc.page_content for doc in docs])
    #print(docs_page_content)
    llm = OpenAI(model='text-davinci-003')
    prompt = PromptTemplate(
        input_variables=["question","docs"],
        template="""
            You are a helpful YouTube assistant that that can answer questions about videos based on the video's transcript.
            
            Answer the following question: {question}
            By searching the following video transcript: {docs}
            
            Only use the factual information from the transcript to answer the question.
            If you feel like you don't have enough information to answer the question, say "I don't know"
            Your answers should be detailed.
            """
    )
    chain = LLMChain(llm=llm,prompt=prompt)
    
    response = chain.run(question=query,docs=docs_page_content)
    response = response.replace("\n"," ")
    return response ,docs

if __name__ == "__main__":
    # print(generate_pet_name("cat","balck"))
    # langchain_agent()
    video_url = "https://www.youtube.com/watch?v=lG7Uxts9SXs"
    db = create_vector_db_from_youtube(video_url)
    response,docs = get_response_from_query(db,"What is the average age of a dog?")