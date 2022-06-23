# Good starting point https://github.com/ucg8j/awesome-dash
# Getting started https://docs.streamlit.io/library/get-started/
# Layout: https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
# Wordcloud: https://discuss.streamlit.io/t/how-to-add-wordcloud-graph-in-streamlit/818/3

import streamlit as st
from PIL import Image

# Run command "py -m streamlit run app.py"
if __name__ == "__main__":

    st.set_page_config(
        page_title="moonpass.ai Dashboard",
        page_icon=":moon",
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

    image_projects = Image.open('img/projects.png')
    image_rocket = Image.open('img/rocket.png')

    # FIXME: Make images clickable and navigate to sidebar options
    #  https://docs.streamlit.io/library/get-started/multipage-apps
    #  https://discuss.streamlit.io/t/side-by-side-clicks-to-switch-between-pages/9473/2
    #  https://discuss.streamlit.io/t/how-can-i-add-a-url-link-to-an-image/13997
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.header("Top Web3 Project")
            st.image(image=image_projects, use_column_width='auto')

        with col2:
            st.header("Trending Projects")
            st.image(image=image_rocket, use_column_width='auto')

