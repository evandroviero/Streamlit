import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide",page_title="Relatorio de Vendas", page_icon="📈")

class Dashboard():
    def __init__(self) -> None:
        self.file = 'data/sales.csv'
    
    @st.cache_data
    def load_csv(self):
        df = pd.read_csv(self.file)
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Year"] = df["Order Date"].dt.year.astype(str)
        return df
    
    def side_bar(self, df):
        with st.sidebar:
            st.title("Relatorio de Vendas")
            distinct_regions = df["Region"].unique().tolist()
            region_selected = st.multiselect("Região", distinct_regions)
            item_type = st.multiselect("Item",df["Item Type"].unique().tolist())
            if region_selected:
                df = df.loc[df["Region"].isin(region_selected)]
            if item_type:
                df = df.loc[df["Item Type"].isin(item_type)]
        return df
    
    def line_chart(self, df):
        df = df.groupby('Year')['Total Profit'].sum().reset_index()
        return df
        
    

    def graphic(self, df):
        st.write("Lucro por País")
        st.bar_chart(df, x="Country", y="Total Profit")
        line = self.line_chart(df)
        st.line_chart(line, x='Year',y='Total Profit')
        # st.pyplot(self.graphic_pie(df))
    

    def run_dashboard(self):
        df = self.load_csv()
        df = self.side_bar(df)
        self.graphic(df)
        st.write(df)
        # st.dataframe(df_line, use_container_width=True)

if __name__ == "__main__":
    Dashboard().run_dashboard()
