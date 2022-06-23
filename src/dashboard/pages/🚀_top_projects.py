import streamlit as st

st.markdown("# Top Projects 🚀")
st.sidebar.markdown("# Top Projects 🚀")

option = st.selectbox(
     'Which top projects would you like to see?',
     ('Top 10 cryptocurrencies', 'Top 10 NFT projects'))

st.write('You selected:', option)

with st.expander("See explanation"):
    st.write("""
         The chart above shows some numbers I picked for you.
         I rolled actual dice for these, so they're *guaranteed* to
         be random.
     """)
    st.image("https://static.streamlit.io/examples/dice.jpg")
