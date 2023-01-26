import streamlit as st
import definitions
from testrading.orm import connector
from testrading.app.repo import repo

# TODO: Implement login


class DashboardRender:

    def __init__(self):
        pass

    def render(self):
        # st.set_page_config(layout="wide")
        st.title('Testrading')

        st.sidebar.title('Navigation')
        st.sidebar.markdown("# Main page")


if 'dashboard' not in st.session_state:
    st.session_state.dashboard = DashboardRender()
    wep = repo.db()
    print(type(wep))

st.session_state.dashboard.render()