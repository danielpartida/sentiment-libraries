import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from wordcloud import WordCloud

st.markdown("# Top Projects 🚀")
st.sidebar.markdown("# Top Projects 🚀")

crypto = 'Top 10 cryptocurrencies'
cryptos = ("BTC", "ETH", "BNB", "ADA", "XRP", "SOL", "DOGE", "DOT", "TRX", "AVAX")

nft = 'Top 10 NFT projects'
nfts = ("BAYC", "CryptoPunks", "Azukis", "Nouns", "Moonbirds", "Meebits",
        "Doodles", "Goblintown", "ArtBlocks", "CloneX")

# TODO: Change this chart with real data
area_chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['positive', 'neutral', 'negative'])

bar_chart_data = pd.DataFrame(
    np.random.randint(low=10, high=500, size=30),
    columns=["count"])

pie_labels = 'Positive', 'Negative', 'Neutral'
pie_sizes = [15, 30, 55]

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        option = st.selectbox(
            'What category? 🤔',
            (crypto, nft))

        st.subheader("24h project sentiment")
        fig1, ax1 = plt.subplots()
        colors = ['#8EB897', '#DD7596', '#B7C3F3']
        ax1.pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=colors,
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}, labeldistance=1.15)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

    with col2:
        if option == crypto:
            project_option = st.selectbox(
                'Which top crypto project? 💸 ',
                cryptos)

        elif option == nft:
            project_option = st.selectbox(
                'Which top NFT project? 🎭',
                nfts
            )

        text = 'Bitcoin, wagmi, LFG, BTC, gg, HODL, hodlers, BTC, crypto, community, community, offchain, onchain,' \
               'moonpass, moonpass, analytics, moonpass, wagmi, cope, ETH, satoshi, recover, offchain, correlation,' \
               'analytics, moonpass, wagmi, superforecasting, fundamentals, fundamentals, team, credibility, ' \
               'experience, investors, moonpass, prediction, time, quality, quantity, gm, gm, gm, team, LFG, Vitalik'
        wordcloud = WordCloud(background_color="white").generate(text)
        fig1, ax1 = plt.subplots()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(wordcloud)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.subheader("24h project topics")
        st.pyplot()

    st.subheader("Sentiment development for {0}".format(project_option))
    st.area_chart(data=area_chart_data, use_container_width=True)
    st.caption("Caption")

    st.subheader("Tweet counts for {0}".format(project_option))
    st.bar_chart(data=bar_chart_data, use_container_width=True)

if option == crypto and project_option:
    st.sidebar.markdown("# {0} 💸".format(project_option))

elif option == nft and project_option:
    st.sidebar.markdown("# {0} 🎭".format(project_option))
