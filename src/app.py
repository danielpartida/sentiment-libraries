# Good starting point https://github.com/ucg8j/awesome-dash
# Getting started https://docs.streamlit.io/library/get-started/

import pandas as pd
import streamlit as st
import numpy as np

if __name__ == "__main__":

    # Run command "py -m streamlit run hello.py"

    st.write("Here's our first attempt at using data to create a table:")

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon'])

    st.map(map_data)

    x = st.slider('x')  # 👈 this is a widget
    st.write(x, 'squared is', x * x)
    st.text_input("Your name", key="name")

    if st.checkbox('Show dataframe'):
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c'])

        chart_data

    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40]
    })

    option = st.selectbox(
        'Which number do you like best?',
        df['first column'])

    'You selected: ', option