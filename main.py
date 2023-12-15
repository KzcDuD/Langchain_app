import streamlit as st
from DocumentChain.documentchain import docxchain
import textwrap

st.title("DocumentChain")
st.subheader("A simple document search engine")

with st.sidebar:
    with st.form(key="my_from"):
        query = st.text_area(
            label = "What is your question?",
            max_chars=100,
            key = "query"
        )

        submit_button = st.form_submit_button(label="Submit")

if query:
    chain = docxchain('data/',query)
    st.text(textwrap.fill(chain.response(),width=85))