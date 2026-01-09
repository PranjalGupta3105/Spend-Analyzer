import streamlit as st
import pandas as pd
import plotly.express as px

conn = st.connection("sql", type="sql", driver="psycopg2", ttl = 10)

st.set_page_config(
    page_title="Method Spend Analytics",
    page_icon=":material/money:",  # Or ":material/home:"
)

st.title("Method Analytics")

st.header("Spends Through All Methods in All Time")


## Spend made in all time through all methods ---------------------------------------------------------------------------------------------
overall_spent_data = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT method_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE is_deleted = 0 AND is_repayed = 0 GROUP BY method_id)e LEFT JOIN payment_methods pm ON e.method_id = pm.id;")

pie_chart_data = {
    "Method Name": overall_spent_data["method_name"],
    "Total Amount": overall_spent_data["total_amount"]
}

dataframe = pd.DataFrame(pie_chart_data)

fig = px.pie(dataframe, values='Total Amount', names='Method Name', title='')

st.plotly_chart(fig)

## Spend made through all methods in a particular year ---------------------------------------------------------------------------------------------
st.markdown("---")
year_options = list(range(2024, pd.Timestamp.now().year + 1))

st.markdown("**<span style='font-size:1.5em'>Select Year</span>**", unsafe_allow_html=True)
selected_year = st.selectbox("", options=year_options, index=len(year_options)-1)
st.markdown("---")

st.header(f"Spends Through All Methods In the Year {selected_year}")

overall_spent_in_year_data = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT method_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY method_id)e LEFT JOIN payment_methods pm ON e.method_id = pm.id;")

st.bar_chart(data=overall_spent_in_year_data, x="method_name", y="total_amount", x_label="Method Name", y_label="Total Amount", sort=False)

## Spend made through all methods in a particular year and month ---------------------------------------------------------------------------------------------
st.markdown("---")
month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

st.markdown("**<span style='font-size:1.5em'>Select Month</span>**", unsafe_allow_html=True)
selected_month = st.selectbox("", options=month_order, index=month_order.index("January"))
st.markdown("---")

st.header(f"Spends Through All Methods In the Year {selected_year} And Month {selected_month}")

overall_spent_in_year_and_month_data = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT method_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = '{selected_year}' AND EXTRACT(MONTH FROM date) = '{month_order.index(selected_month)+1}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY method_id)e LEFT JOIN payment_methods pm ON e.method_id = pm.id;")

pie_chart_data = {
    "Method Name": overall_spent_in_year_and_month_data["method_name"],
    "Total Amount": overall_spent_in_year_and_month_data["total_amount"]
}

dataframe = pd.DataFrame(pie_chart_data)

fig = px.pie(dataframe, values='Total Amount', names='Method Name', title='')

st.plotly_chart(fig)

## Spend made through a particular method in all time ---------------------------------------------------------------------------------------------
st.markdown("---")
method_options = overall_spent_data['method_name'].unique()

st.markdown("**<span style='font-size:1.5em'>Select Method</span>**", unsafe_allow_html=True)
selected_method = st.selectbox("", options=method_options)
st.markdown("---")

st.header(f"Spends Through {selected_method} in All Time")

selected_method_id = overall_spent_data[overall_spent_data['method_name'] == selected_method]['method_id'].values[0]

method_spends_over_years = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT EXTRACT(YEAR FROM date) cal_year, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE method_id = {selected_method_id} AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(YEAR FROM date))e LEFT JOIN payment_methods pm ON pm.id = {selected_method_id} ORDER BY cal_year;")

st.line_chart(data=method_spends_over_years, x="cal_year", y="total_amount", x_label="Year", y_label="Total Amount")

## Spend made through a particular method in a particular year ---------------------------------------------------------------------------------------------
st.header(f"Overall Spends Through {selected_method}, over the months in the year {selected_year}")

method_spends_over_months_in_year = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT EXTRACT(MONTH FROM date) cal_month, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE method_id = {selected_method_id} AND EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(MONTH FROM date))e LEFT JOIN payment_methods pm ON pm.id = {selected_method_id} ORDER BY cal_month;")

st.bar_chart(data=method_spends_over_months_in_year, x="cal_month", y="total_amount", x_label="Month", y_label="Total Amount", sort=False)
