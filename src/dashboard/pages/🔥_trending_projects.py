import streamlit as st
from matplotlib import pyplot as plt
from wordcloud import WordCloud

st.markdown("# Trending Projects 🔥️")
st.sidebar.markdown("# Trending Projects 🔥️️")

pie_labels = 'Positive', 'Negative', 'Neutral'
pie_sizes = [35, 15, 50]

with st.container():
    st.subheader("{}K crypto tweets analyzed in the last 1h".format(31.6))

    token1, token2, token3, token4, token5 = st.columns(5)
    token1.metric("BTC", "{0}K".format(14.6), "1.2 °F")
    token2.metric("ETH", "{0}K".format(10.3), "4%")
    token3.metric("BNB", "{0}K".format(4.1), "-8%")
    token4.metric("DOGE", "{0}K".format(1.4), "-8%")
    token5.metric("SOL", "{0}K".format(1.2), "-8%")

    col1, col2 = st.columns(2)

    with col1:
        text = 'BTC, wagmi, LFG, BTC, gg, HODL, hodlers, BTC, crypto, community, community, USDC, USDC, USDC' \
               'moonpass, moonpass, AVAX, moonpass, move2earn, gm, ETH, satoshi, SOL, punks, BAYC, USDT, punks, BAYC' \
               'analytics, move2earn, wagmi, superforecasting, cycle, moonbirds, Solana, NFT, airdrop, CBDC, ETH, ADA,'\
               'DOT, DOT, moonpass, NFT, DeFi, DeFi, gm, move2earn, gm, team, LFG, ETHBerlin, merge, merge, SOL, Tezos'
        wordcloud = WordCloud(background_color="white").generate(text)
        fig1, ax1 = plt.subplots()
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout()
        plt.imshow(wordcloud)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.subheader("web3 topics in last 1h")
        st.pyplot()

    with col2:
        st.subheader("web3 sentiment in last 1h")
        fig1, ax1 = plt.subplots()
        colors = ['#8EB897', '#DD7596', '#B7C3F3']
        ax1.pie(pie_sizes, labels=pie_labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=colors,
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}, labeldistance=1.15)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

st.sidebar.markdown("# #1 BAYC")
st.sidebar.markdown("# #2 cryptopunks")
st.sidebar.markdown("# #3 Solana")
st.sidebar.markdown("# #4 Move2Earn")
st.sidebar.markdown("# #5 StepN")
