import streamlit as st

st.markdown("# Top Projects 🚀")
st.sidebar.markdown("# Top Projects 🚀")

crypto = 'Top 10 cryptocurrencies'
cryptos = ("BTC", "ETH", "BNB", "ADA", "XRP", "SOL", "DOGE", "DOT", "TRX", "AVAX")

nft = 'Top 10 NFT projects'
nfts = ("BAYC", "CryptoPunks", "Azukis", "Nouns", "Moonbirds", "Meebits",
        "Doodles", "Goblintown", "ArtBlocks", "CloneX")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        option = st.selectbox(
            'What category? 🤔',
            (crypto, nft))

    with col2:
        if option == crypto:
            st.selectbox(
                'Which top crypto project? 💸 ',
                cryptos)

        elif option == nft:
            st.selectbox(
                'Which top NFT project? 🎭',
                nfts
            )
