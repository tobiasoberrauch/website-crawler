import streamlit as st
import pandas as pd

# load xlsx file and show it in a table
st.title('Load xlsx file and show it in a table')

# load xlsx file
df = pd.read_json('data.json')

# show table
st.table(df)
