import streamlit as st

st.set_page_config(page_title="AI Search", layout="centered")
st.title("Business Standard AI Search")

st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        padding: 0.75em;
        background-color: #0a84ff;
        color: grey;
        font-size: 16px;
        border-radius: 10px;
    }
    .stTextInput>div>Input {
        padding: 0.75em;
        font-size: 16px;
        border-radius: 10px;  
    }
</style>
""", unsafe_allow_html=True )

query = st.text_input("What is your query of the day?")

