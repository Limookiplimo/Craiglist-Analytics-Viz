import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Craiglist.csv")
    result = df[["price", "type", "condition", "posting_year"]]
    return result

def type_section(result):
    st.title("Sales by Type")
    st.markdown("##")
    type_options = result["type"].unique()
    default_type = ["sedan"]

    for default_model in default_type:
        if default_model not in type_options:
            default_type.remove(default_model)
    type = st.sidebar.multiselect("Select Type:",options=type_options, default=default_type)
    df_selection = result.query("type == @type")
    return df_selection

@st.cache_data
def display_kpis(df_selection):
    total_sales = int(df_selection["price"].sum())
    total_vehicles = df_selection["posting_year"].count()

    left_column,right_column = st.columns(2)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"${total_sales:,}")
    with right_column:
        st.subheader("Total Vehicles:")
        st.subheader(f"{total_vehicles}")

    st.markdown("---")

@st.cache_data
def display_sales_dashboard(df_selection):
    st.subheader("Sales Dashboard")
    yearly_sum = df_selection.groupby('posting_year')['price'].sum().reset_index()
    fig_veh_type = px.line(yearly_sum,x="posting_year",y="price",template="plotly_white")

    fig_veh_type.update_xaxes(title_text='Posting Year')
    fig_veh_type.update_yaxes(title_text='Total Sales')
    fig_veh_type.update_layout(plot_bgcolor="rgba(0,0,0,0)",xaxis=(dict(showgrid=False)))

    st.plotly_chart(fig_veh_type)
    st.markdown("---")

@st.cache_data
def display_metric_bar_sales(df_selection):
    st.subheader("Metrics Bar")
    yearly_sum = df_selection.groupby('posting_year')['price'].sum().reset_index()
    sales_metric_df = yearly_sum.unstack().unstack().reset_index(drop=True)
    st.write(sales_metric_df)

@st.cache_data
def display_vehicle_type_dashboard(df):
    st.subheader("Vehicle Condition")
    type_condition = df.groupby(["condition", "type"]).size().reset_index(name="count")
    colors = {
        "excellent": "green",
        "good": "blue",
        "fair": "orange",
        "like new": "purple",
        "new": "red",
        "salvage": "gray",
        " SL550": "yellow"
    }

    fig_type_condition = px.bar(type_condition, x="type", y="count", template="plotly_white",color="condition", color_discrete_map=colors)
    fig_type_condition.update_xaxes(title_text='Vehicle Type')
    fig_type_condition.update_yaxes(title_text='Total Vehicles')
    fig_type_condition.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=(dict(showgrid=False)))

    st.plotly_chart(fig_type_condition)
    st.markdown("---")

@st.cache_data
def display_metric_bar_condition(df):
    st.subheader("Metrics Bar")
    type_condition = df.groupby(["condition", "type"]).size().reset_index(name="count")
    type_df = type_condition.unstack().unstack().reset_index(drop=True)
    st.write(type_df)

if __name__ == "__main__":
    df = load_data()
    df_selection = type_section(df)
    display_kpis(df_selection)
    display_sales_dashboard(df_selection)
    display_metric_bar_sales(df_selection)
    display_vehicle_type_dashboard(df)
    display_metric_bar_condition(df)


