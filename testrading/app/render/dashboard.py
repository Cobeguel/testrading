import streamlit as st
import definitions
from testrading.orm import connector

# Initialize sqlalchemy connection
conn = connector.AlchemyConn(connector.DBCredentials(definitions.DB_CONFIG_FILE).__str__())

st.set_page_config(layout="wide")
st.title('Testrading')

st.sidebar.title('Navigation')
st.sidebar.markdown("# Main page")

# TODO: Implement login