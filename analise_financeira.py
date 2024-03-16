import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide",page_title="Relatorio de Vendas", page_icon="📈")


file = 'data/sales.csv'
    
@st.cache_data
def load_csv():
    df = pd.read_csv(file)
    return df

def ajusta_coluna(df):
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year.astype(str)
    return df

def side_bar(df):
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

def line_chart(df):
    df = df.groupby('Year')['Total Profit'].sum().reset_index()
    return df
    


def graphic(df):
    st.write("Lucro por País")
    st.bar_chart(df, x="Country", y="Total Profit")
    line = line_chart(df)
    st.line_chart(line, x='Year',y='Total Profit')
    # st.pyplot(graphic_pie(df))


def run_dashboard():
    df = load_csv()
    df = ajusta_coluna(df)
    df = side_bar(df)
    graphic(df)
    st.write(df)
    # st.dataframe(df_line, use_container_width=True)

if __name__ == "__main__":
    run_dashboard()
