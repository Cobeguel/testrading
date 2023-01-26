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

    def __sidebar(self):
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

    def update(self):
        self.providers.update_data(self.__fetch_providers())
        self.providers()

    def insert_provider(name):
        if name == "":
            st.warning("Provider name can't be empty", icon="⚠️")
        else:
            with repo.db().get_session() as sess:
                provider = financial.Provider(name=name)
                sess.add(provider)
                sess.commit()

    def render(self):
        st.markdown("# Data Manager")
        st.sidebar.markdown("# Load data")

        st.markdown("## Providers")
        #self.providers = st.empty
        self.providers = components.DFpaginated(self.__fetch_providers())
        self.providers.render()
        with st.form(key="provider_create_form", clear_on_submit=True):
            provider_name = st.text_input('Add provider', placeholder='provider name')
            submit_button = st.form_submit_button(label="Create")
            if submit_button:
                if provider_name == "":
                    st.warning("Provider name can't be empty", icon="⚠️")
                else:
                    with repo.db().get_session() as sess:
                        db_provider = sess.query(
                            financial.Provider).filter(financial.Provider.name == provider_name).all()
                        if len(db_provider) != 0:
                            st.warning(f'Provider: {provider_name} already exists', icon="⚠️")
                        else:
                            provider = financial.Provider(name=provider_name)
                            sess.add(provider)
                            sess.commit()
                            #st.success(f'Provider: {provider_name} have been created!', icon="✅")
                            st.experimental_rerun()

        st.markdown("## Assets")
        assets = st.empty
        assets = components.DFpaginated(self.__fetch_assets())
        assets.render()
        with st.form(key="asset_create_form", clear_on_submit=True):
            asset_name = st.text_input('Add asset', placeholder='asset name')
            submit_button = st.form_submit_button(label="Create")
            if submit_button:
                if asset_name == "":
                    st.warning("Asset name can't be empty", icon="⚠️")
                else:
                    with repo.db().get_session() as sess:
                        db_asset = sess.query(financial.Asset).filter(financial.Asset.name == asset_name).all()
                        if len(db_asset) != 0:
                            st.warning(f'Asset: {asset_name} already exists', icon="⚠️")
                        else:
                            asset = financial.Asset(name=asset_name)
                            sess.add(asset)
                            sess.commit()
                            #st.success(f'Market: {market_name} have been created!', icon="✅")

        st.markdown("## Upload data")

        col1, col2 = st.columns(2)
        providers = ['']
        with repo.db().get_session() as sess:
            providers = [provider.name for provider in sess.query(financial.Provider).all()]
        provider_select = col1.selectbox('Select provider', providers)
        data_type = col1.radio("Data type", ('OHLCV', 'Tick', 'Trades'))
        symbol = col1.text_input('Symbol', placeholder='symbol')
        assets = ['']
        with repo.db().get_session() as sess:
            assets = [provider.name for provider in sess.query(financial.Asset).all()]
        asset = col1.selectbox('Select asset', assets)

        file_separator = col2.text_input("Separator", value=";", max_chars=1)
        header = col2.number_input("Header", min_value=0, value=0)

        uploaded_file = st.file_uploader("Upload a file")
        sample = st.empty()
        time_mapper, open_mapper, high_mapper, low_mapper, close_mapper, volume_mapper = st.columns(6)
        time_col = open_col = high_col = low_col = close_col = ""
        data = None
        if uploaded_file is not None:
            try:
                csv_header = header if header != 0 else None
                data = pd.read_csv(uploaded_file, sep=file_separator, header=csv_header)
                sample_data = data.head(10)
            except ValueError as error:
                errormsg = "Cannot load file: " + str(error)
                st.error(errormsg, icon="⚠️")
            sample.write(sample_data)
            st.write("Column mapper")
            map_options = sample_data.columns.tolist()
            if len(map_options) < 4:
                st.warning("File must have at least time, open, high, low, and close columns", icon="⚠️")
            else:
                time_col = time_mapper.selectbox("Time", map_options, index=0)
                open_col = open_mapper.selectbox("Open", map_options, index=1)
                high_col = high_mapper.selectbox("High", map_options, index=2)
                low_col = low_mapper.selectbox("Low", map_options, index=3)
                close_col = close_mapper.selectbox("Close", map_options, index=4)
                if len(map_options) > 5:  # Adjust to be optional
                    volume_mapper.selectbox("Volume", map_options, index=5)

        submit_button = st.button(label="Upload")
        if submit_button:
            if uploaded_file is None:
                st.warning("File is empty", icon="⚠️")
            else:
                if provider_select == "":
                    st.warning("Provider is empty", icon="⚠️")
                elif symbol == "":
                    st.warning("Symbol is empty", icon="⚠️")
                elif time_col == "" or open == "" or high_col == "" or low_col == "" or close_col == "":
                    st.warning("Column mapper is incomplete", icon="⚠️")
                else:
                    csv_header = header if header != 0 else None
                    #data = pd.read_csv(uploaded_file, sep=file_separator, header=csv_header)
                    data = data.rename(columns={
                        time_col: "datetime",
                        open_col: "open",
                        high_col: "high",
                        low_col: "low",
                        close_col: "close",
                    })
                    # data.dropna()
                    data['datetime'] = pd.to_datetime(data['datetime'])
                    data.set_index('datetime', drop=True)
                    data = data.sort_values(by='datetime')
                    data['id'] = [str(Ksuid()) for _ in range(len(data.index))]
                    data['asset'] = asset.upper()
                    data['provider'] = provider_select.upper()
                    data['symbol'] = symbol.upper()
                    data['resolution'] = data['datetime'].diff().dt.total_seconds().value_counts().nlargest(
                        1).index.astype(int)[0]
                    data['create_time'] = datetime.datetime.now()
                    data = data.drop(columns=[5])
                    with repo.db().get_conn() as conn:
                        data.to_sql('ohlcv', con=conn, if_exists='append', index=False)
                    st.success("File uploaded", icon="✅")

    # Is possible to deprecate this part
    def __print_sample(self, file, sample_widget, separator, header):
        try:
            csv_header = header if header != 0 else None
            sample_data = pd.read_csv(file, nrows=10, sep=separator, header=csv_header)
        except ValueError as error:
            errormsg = "Cannot load file: " + str(error)
            st.error(errormsg, icon="⚠️")
        sample_widget.write(sample_data)
