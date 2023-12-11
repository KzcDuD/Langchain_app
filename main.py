from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

def generate_pet_name(animal_type,pet_color):
    llm =OpenAI(temperature =0.7) # The model creative temperature
    prompt_template_name = PromptTemplate(
        input_variables =['animal_type'],
        template="I have a {animal_type} pet and I want a coll name for it , it is {pet_color} in color. Suggest me five cool names for my pet."
    )
    name_chain = LLMChain(llm=llm,prompt=prompt_template_name)
    response =  name_chain({'animal_type':animal_type,'pet_color':pet_color})
    
    return response
    
if __name__ == "__main__":
    print(generate_pet_name("cat","balck"))