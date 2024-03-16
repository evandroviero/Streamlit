import streamlit as st
import pandas as pd
import numpy as np
import re

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

def get_values(df):
    total_revenue = round(df['Total Revenue'].sum(),2)
    order = df.groupby(['Order Priority'])['Total Revenue'].sum().reset_index()
    
    order_c = order.loc[order['Order Priority'] == 'M', ['Total Revenue']].values[0][0]
    order_h = order.loc[order['Order Priority'] == 'H', ['Total Revenue']].values[0][0]
    order_m = order.loc[order['Order Priority'] == 'M', ['Total Revenue']].values[0][0]
    order_l = order.loc[order['Order Priority'] == 'L', ['Total Revenue']].values[0][0]

    return order_c, order_h, order_m, order_l, total_revenue

def formatar_numero(numero):
    if abs(numero) >= 1e9:
        return "{:.2f}B".format(numero / 1e9)
    elif abs(numero) >= 1e6:
        return "{:.2f}M".format(numero / 1e6)
    elif abs(numero) >= 1e3:
        return "{:.2f}K".format(numero / 1e3)
    else:
        return str(numero)
    
def kpi(df):
    st.write("Prioridade")
    col1, col2, col3, col4, col5 = st.columns(5)
    order_c, order_h, order_m, order_l, total_revenue= get_values(df)
    col1.metric("Total Vendas", formatar_numero(total_revenue))
    col2.metric("Critical", formatar_numero(order_c), round(order_c/total_revenue * 100,2), delta_color="off")
    col3.metric("High", formatar_numero(order_h), round(order_h/total_revenue * 100,2), delta_color="off")
    col4.metric("Medium", formatar_numero(order_m), round(order_m/total_revenue * 100,2), delta_color="off")
    col5.metric("Low", formatar_numero(order_l), round(order_l/total_revenue * 100,2), delta_color="off")

    return df

def centralizar_texto(texto):
    return f"<div style='text-align:center'>{texto}</div>"

def graphic(df):
    kpi(df)
    st.write(centralizar_texto("Lucro por País"),unsafe_allow_html=True)
    st.bar_chart(df, x="Country", y="Total Profit")
    line = line_chart(df)
    st.write(centralizar_texto("Lucro por Ano"),unsafe_allow_html=True)
    st.line_chart(line, x='Year',y='Total Profit')
    

def run_dashboard():
    df = load_csv()
    df = ajusta_coluna(df)
    df = side_bar(df)
    graphic(df)
    st.write(df)

if __name__ == "__main__":
    run_dashboard()
