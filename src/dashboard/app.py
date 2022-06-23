# Good starting point https://github.com/ucg8j/awesome-dash
# Getting started https://docs.streamlit.io/library/get-started/
# Layout: https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
# Wordcloud: https://discuss.streamlit.io/t/how-to-add-wordcloud-graph-in-streamlit/818/3

import pandas as pd
import streamlit as st
import numpy as np

# Run command "py -m streamlit run app.py"
if __name__ == "__main__":

    st.set_page_config(
        page_title="moonpass.ai Dashboard",
        page_icon="random",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'Get Help': 'https://www.moonpass.ai',
            'Report a bug': None,
            'About': "# Alpha dashboard of moonpass.ai 🌚🧭!"
        }
    )

    st.markdown("# Mooonpass Dashboard 🌚🧭")
    st.sidebar.markdown("# Main page 🌚🧭")
