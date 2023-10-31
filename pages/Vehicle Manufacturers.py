import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Craiglist.csv")
    result = df[["price", "manufacturer", "model", "posting_year"]]
    return result

def manufacturer_section(data):
    st.title("Sales by Manufacturer")
    st.markdown("##")
    man_options = data["manufacturer"].unique()
    default_man = ["bmw"]
    
    for default_model in default_man:
        if default_model not in man_options:
            default_man.remove(default_model)
    manufacturer = st.sidebar.multiselect("Select Manufacturer:",options=man_options, default=default_man)
    df_selection = data.query("manufacturer == @manufacturer")
    return df_selection

@st.cache_data
def display_kpis(df_selection):
    total_sales = int(df_selection["price"].sum())
    total_models = df_selection["model"].nunique()
    total_vehicles = df_selection["posting_year"].count()
    left_column, middle_column, right_column = st.columns(3)
    
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"${total_sales:,}")
    with middle_column:
        st.subheader("Total Models:")
        st.subheader(f"{total_models}")
    with right_column:
        st.subheader("Total Vehicles:")
        st.subheader(f"{total_vehicles}")

@st.cache_data
def display_sales_dashboard(df_selection):
    yearly_sum = df_selection.groupby('posting_year')['price'].sum().reset_index()
    fig_veh_man = px.line(yearly_sum,x="posting_year",y="price",template="plotly_white")
    
    fig_veh_man.update_xaxes(title_text='Posting Year')
    fig_veh_man.update_yaxes(title_text='Total Sales')
    fig_veh_man.update_layout(plot_bgcolor="rgba(0,0,0,0)",xaxis=dict(showgrid=False))
    
    st.markdown("---")
    st.plotly_chart(fig_veh_man)
    st.markdown("---")

@st.cache_data
def display_metric_bar(df_selection):
    st.subheader("Metrics Bar")
    yearly_sum = df_selection.groupby('posting_year')['price'].sum().reset_index()
    metrics_df = yearly_sum.unstack().unstack().reset_index(drop=True)
    st.write(metrics_df)

if __name__ == "__main__":
    df = load_data()
    df_selection = manufacturer_section(df)
    display_kpis(df_selection)
    display_sales_dashboard(df_selection)
    display_metric_bar(df_selection)