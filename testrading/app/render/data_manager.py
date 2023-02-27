import streamlit as st
import pandas as pd
import datetime

from testrading.app.repo import repo
from testrading.models import financial
from testrading.app.render import components
from ksuid import Ksuid


class DataManagerRender():

    def __init__(self) -> None:
        self.components = {}
        pass

    def __fetch_providers(self):
        with repo.db().get_conn() as conn:
            df = pd.read_sql("select * from providers", conn)
            conn.close()
            return df

    def __fetch_assets(self):
        with repo.db().get_conn() as conn:
            df = pd.read_sql("select * from assets", conn)
            conn.close()
            return df

    def render(self):
        st.markdown("# Data Manager")
        st.sidebar.markdown("# Load data")

        st.markdown("## Providers")
        self.providers = components.DFpaginated(self.__fetch_providers())
        self.providers.render()
        with st.form(key="provider_create_form", clear_on_submit=True):
            provider_name = st.text_input('Add provider', placeholder='provider name')
            submit_button = st.form_submit_button(label="Create")
            if submit_button:
                if provider_name == "":
                    st.error("Provider name cannot be empty", icon="🚨")
                else:
                    with repo.db().get_session() as sess:
                        db_provider = sess.query(financial.Provider).filter(financial.Provider.name == provider_name).all()
                        if len(db_provider) != 0:
                            st.error(f'Provider: {provider_name} already exists', icon="🚨")
                        else:
                            provider = financial.Provider(name=provider_name)
                            sess.add(provider)
                            sess.commit()
                            st.experimental_rerun()
                            #st.success(f'Provider: {provider_name} have been created!', icon="✅")

        st.markdown("## Assets")
        assets = st.empty
        assets = components.DFpaginated(self.__fetch_assets())
        assets.render()
        with st.form(key="asset_create_form", clear_on_submit=True):
            asset_name = st.text_input('Add asset', placeholder='asset name')
            submit_button = st.form_submit_button(label="Create")
            if submit_button:
                if asset_name == "":
                    st.error("Asset name cannot be empty", icon="🚨")
                else:
                    with repo.db().get_session() as sess:
                        db_asset = sess.query(financial.Asset).filter(financial.Asset.name == asset_name).all()
                        if len(db_asset) != 0:
                            st.error(f'Asset: {asset_name} already exists', icon="🚨")
                        else:
                            asset = financial.Asset(name=asset_name)
                            sess.add(asset)
                            sess.commit()
                            st.experimental_rerun()
                            #st.success(f'Market: {market_name} have been created!', icon="✅")

        st.markdown("## Upload data")

        col1, col2 = st.columns(2)

        # Left column
        providers = ['']
        with repo.db().get_session() as sess:
            providers = [provider.name for provider in sess.query(financial.Provider).all()]
        data_type = col1.radio("Data type", ('OHLCV', 'Tick'))
        provider_select = col1.selectbox('Select provider', providers)
        symbol = col1.text_input('Symbol', placeholder='symbol')
        assets = ['']
        with repo.db().get_session() as sess:
            assets = [provider.name for provider in sess.query(financial.Asset).all()]
        asset = col1.selectbox('Select asset', assets)

        # Right column
        file_separator = col2.text_input("Separator", value=",", max_chars=1)
        header = col2.number_input("Header", min_value=0, value=0)
        date_format = col2.text_input(label="Date format", value="")

        uploaded_file = st.file_uploader("Upload a file")
        sample = st.empty()
        if data_type == 'OHLCV':
            time_mapper, open_mapper, high_mapper, low_mapper, close_mapper, volume_mapper = st.columns(6)
            time_col = open_col = high_col = low_col = close_col = volume_col = ""
        elif data_type == 'Tick':
            time_mapper, ask_mapper, bid_mapper, volume_mapper = st.columns(4)
            time_col = ask_col = bid_col = volume_col = ""
        data = None

        if uploaded_file is not None:
            try:
                # TODO Add chunksize to read smaller sample.
                csv_header = header if header != 0 else None
                data = pd.read_csv(uploaded_file, sep=file_separator, header=csv_header)
                sample_data = data.head(10)
            except ValueError as error:
                errormsg = "Cannot load file: " + str(error)
                st.error(errormsg, icon="🚨")
            sample.write(sample_data)
            st.write("Column mapper")
            map_options = sample_data.columns.tolist()
            if data_type == 'OHLCV':
                if len(map_options) < 5:
                    st.error("File must have at least time, open, high, low, and close columns", icon="🚨")
                    st.stop()
                else:
                    time_col = time_mapper.selectbox("Time", map_options, index=0)
                    open_col = open_mapper.selectbox("Open", map_options, index=1)
                    high_col = high_mapper.selectbox("High", map_options, index=2)
                    low_col = low_mapper.selectbox("Low", map_options, index=3)
                    close_col = close_mapper.selectbox("Close", map_options, index=4)
                    if len(map_options) > 5:
                        volume_col = volume_mapper.selectbox("Volume", map_options, index=5)
            if data_type == 'Tick':
                if len(map_options) < 3:
                    st.error("File must have at least time, ask, and bid columns", icon="🚨")
                    st.stop()
                else:
                    time_col = time_mapper.selectbox("Time", map_options, index=0)
                    ask_col = ask_mapper.selectbox("Ask", map_options, index=1)
                    bid_col = bid_mapper.selectbox("Bid", map_options, index=2)
                    if len(map_options) > 3:
                        volume_col = volume_mapper.selectbox("Volume", map_options, index=3)

        submit_button = st.button(label="Upload")
        if submit_button:
            if uploaded_file is None:
                st.error("File not found", icon="🚨")
            else:
                try:
                    data[time_col] = pd.to_datetime(data[time_col], format=date_format)
                except ValueError as error:
                    st.error("Time column cannot be casted to datetime", icon="🚨")
                    st.stop()

                if provider_select == "":
                    st.error("Provider is empty", icon="🚨")
                    st.stop()
                elif symbol == "":
                    st.error("Symbol is empty", icon="🚨")
                    st.stop()
                elif data_type == 'OHLCV':
                    if time_col == "" or open_col == "" or high_col == "" or low_col == "" or close_col == "":
                        st.error("Column mapper is incomplete", icon="🚨")
                        st.stop()
                elif data_type == 'Tick':
                    if time_col == "" or ask_col == "" or bid_col == "":
                        st.error("Column mapper is incomplete", icon="🚨")
                        st.stop()

                csv_header = header if header != 0 else None
                if data_type == 'OHLCV':
                    data = data.rename(columns={
                        time_col: "datetime",
                        open_col: "open",
                        high_col: "high",
                        low_col: "low",
                        close_col: "close",
                        volume_col: "volume",
                    })
                elif data_type == 'Tick':
                    data = data.rename(columns={
                        time_col: "datetime",
                        ask_col: "ask",
                        bid_col: "bid",
                        volume_col: "volume",
                    })

                data['datetime'] = pd.to_datetime(data['datetime'])
                data = data.sort_values(by='datetime')
                data['id'] = [str(Ksuid()) for _ in range(len(data.index))]
                data['asset'] = asset.upper()
                data['provider'] = provider_select.upper()
                data['symbol'] = symbol.upper()
                if data_type == 'OHLCV':
                    data['resolution'] = data['datetime'].diff().dt.total_seconds().value_counts().nlargest(1).index.astype(int)[0]
                data['create_time'] = datetime.datetime.now()

                with repo.db().get_conn() as conn:
                    if data_type == 'OHLCV':
                        data.to_sql('ohlcv', con=conn, if_exists='append', index=False)
                    elif data_type == 'Tick':
                        data.to_sql('tick', con=conn, if_exists='append', index=False)

                st.success("File uploaded", icon="✅")
