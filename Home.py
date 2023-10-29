import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title= "Sales Dashboard", page_icon=":bar_chart:", layout="wide")
df = pd.read_csv("Craiglist.csv")


# --- Home Page ---
st.title("Craiglist Analytics")
st.markdown("##")

# KPI's
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

# -- Annual Sales Chart ---
st.subheader(":bar_chart: Annual Sales Dashboard")
annual_sales = (
    df.groupby(by=["posting_year"]).sum()[["price"]].sort_values(by="posting_year")
)
fig_veh_sales = px.bar(
    annual_sales,
    x=annual_sales.index, 
    y="price",
    template="plotly_white",
    )
fig_veh_sales.update_layout(plot_bgcolor="rgba(0,0,0,0)",xaxis=(dict(showgrid=False)))
st.plotly_chart(fig_veh_sales)

st.markdown("---")

# --- Metric Bar ---
st.subheader("Metrics Bar")
new_df = annual_sales.unstack().unstack().reset_index(drop=True).reset_index(drop=True)
new_df




