import pandas as pd
import streamlit as st
import plotly.express as px

# Page setup
st.set_page_config(page_title= "Sales Dashboard", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Craiglist.csv")
    return df

@st.cache_data
def calculate_kpis(df):
    total_sales = int(df["price"].sum())
    total_vehicles = df["posting_date"].count()
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"$ {total_sales:,}")
    with right_column:
        st.subheader("Total Vehicles")
        st.subheader(f"{total_vehicles}")
    
    st.markdown("---")

@st.cache_data
def create_sales_chart(df):
    annual_sales = (df\
        .groupby(by=["posting_year"])\
        .sum()[["price"]]\
        .sort_values(by="posting_year")
    )
    fig_veh_sales = px.bar(
    annual_sales,
    x=annual_sales.index, 
    y="price",
    template="plotly_white",
    )
    fig_veh_sales.update_xaxes(title_text='Posting Year')
    fig_veh_sales.update_yaxes(title_text='Total Sales')
    fig_veh_sales.update_layout(plot_bgcolor="rgba(0,0,0,0)",xaxis=(dict(showgrid=False)))
    st.plotly_chart(fig_veh_sales)

    st.markdown("---")

@st.cache_data
def create_metrics_bar(df):
    annual_sales = (
        df.groupby(by=["posting_year"])
        .sum()[["price"]]
        .sort_values(by="posting_year")
    )
    metrics_df = annual_sales.unstack().unstack().reset_index(drop=True)
    st.write(metrics_df)


if __name__ == "__main__":
    df = load_data()
    calculate_kpis(df)
    create_sales_chart(df)
    create_metrics_bar(df)