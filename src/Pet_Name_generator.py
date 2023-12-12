import src.langchain_helper as lch
import streamlit as st

st.title("Pet Name Generator")

animal_type = st.sidebar.selectbox("What is your pet?",("Cat","Dog","Bird","Rabbit"))

if animal_type =='Cat':
    pet_color = st.sidebar.text_area("What is the color of your cat?",max_chars=10)
    
if animal_type =='Dog':
    pet_color = st.sidebar.text_area("What is the color of your dog?",max_chars=10)

if animal_type =='Bird':
    pet_color = st.sidebar.text_area("What is the color of your bird?",max_chars=10)

if animal_type =='Rabbit':
    pet_color = st.sidebar.text_area("What is the color of your rabbit?",max_chars=10)

if pet_color:
    response = lch.generate_pet_name(animal_type,pet_color)
    # st.text(response)
    st.write("Here are some cool names for your pet:")
    st.write(response['pet_name'])