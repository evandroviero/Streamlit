import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

class Dashboard():
    def __init__(self) -> None:
        self.file = 'data/sales.csv'

    def load_csv(self):
        df = pd.read_csv(self.file)
        df["Order Date"] = pd.to_datetime(df["Order Date"])
        df["Year"] = df["Order Date"].dt.year
        return df
    
    def side_bar(self, df):
        with st.sidebar:
            st.title("Análise de Lucro")
            distinct_regions = df["Region"].unique().tolist()
            region_selected = st.multiselect("Região", distinct_regions)
            item_type = st.multiselect("Item",df["Item Type"].unique().tolist())
            if region_selected:
                df = df.loc[df["Region"].isin(region_selected)]
            if item_type:
                df = df.loc[df["Item Type"].isin(item_type)]
        return df
    
    def graphic_pie(self, df):
        df = df.groupby('Year')['Total Profit'].sum().reset_index()
        labels = df['Year'].tolist()
        sizes = df['Total Profit'].tolist()
        fig, ax = plt.subplots(facecolor='none')
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        return fig
    

    def graphic(self, df):
        st.write("Lucro por País")
        st.bar_chart(df, x="Country", y="Total Profit")
        st.pyplot(self.graphic_pie(df))
    

    def run_dashboard(self):
        df = self.load_csv()
        df = self.side_bar(df)
        self.graphic(df)
        st.write("Database")
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    Dashboard().run_dashboard()
