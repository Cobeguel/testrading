import pandas as pd
import streamlit as st


class DFpaginated:

    def __init__(self, df, page_size=10):
        self.data = df
        self.placeholder = st.empty
        self.page_size = page_size
        self.__calculate_limits__()

    def __calculate_limits__(self):
        self.page_size = self.page_size
        self.page = 0
        self.max_pages = len(self.data) // self.page_size

    def __call__(self):
        return self.data.iloc[self.page * self.page_size:(self.page + 1) * self.page_size]

    def update_data(self, df):
        self.data = df
        self.__calculate_limits__()
        st.write(self())

    def next(self):
        if self.page < self.max_pages:
            self.page += 1

    def prev(self):
        if self.page > 1:
            self.page -= 1

    def render(self):
        # TODO: Adjust columns
        if len(self.data) > self.page_size:
            prev, _, next = st.columns([2, 10, 2])
            if prev.button('Prev'):
                self.prev()
            if next.button('Next'):
                self.next()
        st.write(self())
