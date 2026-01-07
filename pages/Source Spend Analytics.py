import streamlit as st
import pandas as pd
import plotly.express as px

conn = st.connection("sql", type="sql", driver="psycopg", ttl = 10)

st.set_page_config(
    page_title="Source Spend Analytics",
    page_icon=":material/money:",  # Or ":material/home:"
)

st.title("Source Analytics")

st.header("Spends Through All Sources in All Time")


## Spend made in all time through all sources ---------------------------------------------------------------------------------------------
overall_spent_data = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT source_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE is_deleted = 0 AND is_repayed = 0 GROUP BY source_id)e LEFT JOIN payment_sources ps ON e.source_id = ps.id;")

# st.bar_chart(data=overall_spent_data, x="source_name", y="total_amount", x_label="Source Name", y_label="Total Amount", sort=False)

pie_chart_data = {
    "Source Name": overall_spent_data["source_name"],
    "Total Amount": overall_spent_data["total_amount"]
}

dataframe = pd.DataFrame(pie_chart_data)

fig = px.pie(dataframe, values='Total Amount', names='Source Name', title='')

st.plotly_chart(fig)

## Spend made through all sources in a particular year ---------------------------------------------------------------------------------------------
st.markdown("---")
year_options = list(range(2024, pd.Timestamp.now().year + 1))

st.markdown("**<span style='font-size:1.5em'>Select Year</span>**", unsafe_allow_html=True)
selected_year = st.selectbox("", options=year_options, index=len(year_options)-1)
st.markdown("---")

st.header(f"Spends Through All Sources In the Year {selected_year}")

overall_spent_in_year_data = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT source_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY source_id)e LEFT JOIN payment_sources ps ON e.source_id = ps.id;")

st.bar_chart(data=overall_spent_in_year_data, x="source_name", y="total_amount", x_label="Source Name", y_label="Total Amount", sort=False)

## Spend made through all sources in a particular year and month ---------------------------------------------------------------------------------------------
st.markdown("---")
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

st.markdown("**<span style='font-size:1.5em'>Select Month</span>**", unsafe_allow_html=True)
selected_month = st.selectbox("", options=month_order, index=month_order.index("January"))
st.markdown("---")

st.header(f"Spends Through All Sources In the Year {selected_year} And Month {selected_month}")

overall_spent_in_year_and_month_data = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT source_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = '{selected_year}' AND EXTRACT(MONTH FROM date) = '{month_order.index(selected_month)+1}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY source_id)e LEFT JOIN payment_sources ps ON e.source_id = ps.id;")

pie_chart_data = {
    "Source Name": overall_spent_in_year_and_month_data["source_name"],
    "Total Amount": overall_spent_in_year_and_month_data["total_amount"]
}

dataframe = pd.DataFrame(pie_chart_data)

fig = px.pie(dataframe, values='Total Amount', names='Source Name', title='')

st.plotly_chart(fig)

## Spend made through a particular source in all time ---------------------------------------------------------------------------------------------
st.markdown("---")
source_options = overall_spent_data['source_name'].unique()

st.markdown("**<span style='font-size:1.5em'>Select Source</span>**", unsafe_allow_html=True)
selected_source = st.selectbox("", options=source_options)
st.markdown("---")

st.header(f"Spends Through {selected_source} in All Time")

selected_source_id = overall_spent_data[overall_spent_data['source_name'] == selected_source]['source_id'].values[0]

source_spends_over_years = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT EXTRACT(YEAR FROM date) cal_year, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE source_id = {selected_source_id} AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(YEAR FROM date))e LEFT JOIN payment_sources ps ON ps.id = {selected_source_id} ORDER BY cal_year;")

st.line_chart(data=source_spends_over_years, x="cal_year", y="total_amount", x_label="Year", y_label="Total Amount")

## Spend made through a particular source in a particular year ---------------------------------------------------------------------------------------------
st.header(f"Overall Spends Through {selected_source}, over the months in the year {selected_year}")

source_spends_over_months_in_year = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT EXTRACT(MONTH FROM date) cal_month, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE source_id = {selected_source_id} AND EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(MONTH FROM date))e LEFT JOIN payment_sources ps ON ps.id = {selected_source_id} ORDER BY cal_month;")

st.bar_chart(data=source_spends_over_months_in_year, x="cal_month", y="total_amount", x_label="Month", y_label="Total Amount", sort=False)
