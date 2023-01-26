import streamlit as st
import definitions
from testrading.orm import connector


def build_conn() -> connector.AlchemyConn:
    conn = connector.AlchemyConn(connector.DBCredentials(definitions.DB_CONFIG_FILE).__str__())
    return conn


@st.experimental_singleton
def db() -> connector.AlchemyConn:
    return connector.AlchemyConn(connector.DBCredentials(definitions.DB_CONFIG_FILE).__str__())


def add_ohlcv() -> bool:
    pass
