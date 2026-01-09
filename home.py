import streamlit as st
import pandas as pd

conn = st.connection("sql", type="sql", driver="psycopg2")

st.set_page_config(
    page_title="Home",
    page_icon="🏠",  # Or ":material/home:"
)

st.title("Expense Analyzer")

year_options = list(range(2024, pd.Timestamp.now().year + 1))

selected_year = st.selectbox("Select Year", options=year_options, index=len(year_options)-1)

# st.write(f"Selected Year is {selected_year}.")

data = conn.query(f"SELECT EXTRACT(MONTH FROM date) AS month_no,TRIM(TO_CHAR(date, \'Month\')) AS month_name,ROUND(SUM(amount)::numeric, 2) AS total_amount FROM \"public\".\"expenses\" WHERE EXTRACT(YEAR FROM date) = {selected_year} AND is_deleted = 0 AND is_repayed = 0 GROUP BY TO_CHAR(date, \'Month\'), EXTRACT(MONTH FROM date) ORDER BY EXTRACT(MONTH FROM date);")

month_order = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

data["month_name"] = pd.Categorical(data["month_name"], categories=month_order, ordered=True)

st.bar_chart(data=data, x="month_name", y="total_amount", x_label="Month", y_label="Total Amount", sort=False)

selected_month = st.selectbox("Select Month", options=month_order, index=month_order.index("January"))

month_data = conn.query(f"SELECT EXTRACT(DAY FROM date) day_of_month,ROUND(SUM(amount)::numeric, 2) AS total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = {selected_year} AND EXTRACT(MONTH FROM date) = {month_order.index(selected_month)+1} AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(DAY FROM date) ORDER BY EXTRACT(DAY FROM date);")

if not month_data.empty:
    st.line_chart(data=month_data, x="day_of_month", y="total_amount", x_label="Day of Month", y_label="Total Amount")
else:
    st.write(f"No data available for {selected_month} {selected_year}.")

