import streamlit as st
from testrading.app.render import data_manager

if 'data_manager' not in st.session_state:
    st.session_state.data_manager = data_manager.DataManagerRender()

st.session_state.data_manager.render()
