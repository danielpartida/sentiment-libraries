import streamlit as st

st.markdown("# Top Projects 🚀")
st.sidebar.markdown("# Top Projects 🚀")

option = st.selectbox(
     'Which top projects would you like to see?',
     ('Top 10 cryptocurrencies', 'Top 10 NFT projects'))

st.write('You selected:', option)
