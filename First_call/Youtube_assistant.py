import langchain_helper as lch
import streamlit as st
import textwrap

st.title("Youtube Assistant")

with st.sidebar:
    with st.form(key="my_from"):
        youtube_url = st.text_area(
            label = "What is the youtube url?",
            max_chars=50,
        )
        query = st.text_area(
            label = "What is your question?",
            max_chars=50,
            key = "query"
        )

        submit_button = st.form_submit_button(label="Submit")
        
if youtube_url and query:
    db = lch.create_vector_db_from_youtube(youtube_url)
    response,docs = lch.get_response_from_query(db,query)
    st.subheader("Answer:")
    st.text(textwrap.fill(response,width=85))
    