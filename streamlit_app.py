import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Olympic Games Medals",
    page_icon="🥇🥈🥉",
    layout="wide",
    initial_sidebar_state="expanded")

# Sidebar
with st.sidebar:
    st.title('🥇🥈🥉 Olympic Games Medals')

x = st.slider("Select a value")
st.write(x, "squared is", x * x)
