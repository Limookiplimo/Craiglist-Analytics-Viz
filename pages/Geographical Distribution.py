import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Craiglist.csv")
    result = df[["lat", "long", "type","state"]]
    return result

@st.cache_data
def display_geographical_distribution(result):
    st.title("Geographical Distribution")
    st.markdown("##")
    result = result[
        (result['lat'] > 24) & (result['lat'] < 50) &
        (result['long'] > -125) & (result['long'] < -65)
    ]
    fig = px.scatter(result, x="long", y="lat",color="type",labels={"type": "Vehicle Type"},size_max=20)
    fig.update_layout(showlegend=True,legend=dict(title="Vehicle Type",orientation="v",x=-0.5))

    fig.update_xaxes(title_text="Longitude")
    fig.update_yaxes(title_text="Latitude")

    st.plotly_chart(fig)
    st.markdown("---")

@st.cache_data
def display_metrics_bar(result):
    st.subheader("Metrics Bar")
    veh_sum = result.groupby("state").size().reset_index(name="vehicles")
    metrics_table = veh_sum.unstack().unstack().reset_index(drop=True)
    st.write(metrics_table)

if __name__ == "__main__":
    df = load_data()
    display_geographical_distribution(df)
    display_metrics_bar(df)