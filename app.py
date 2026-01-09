import streamlit as st
import pandas as pd
import bcrypt
import jwt
import datetime
import plotly.express as px

# ===================== Authentication Section =====================
JWT_SECRET = st.secrets["auth"]["jwt_secret"]
conn = st.connection("sql", type="sql", driver="psycopg2", ttl=10)

st.set_page_config(
    page_title="Expense Analyzer",
    page_icon="🏠",
    layout="wide"
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_username = None
    st.session_state.jwt_token = None
    st.session_state.page = "Home"

if not st.session_state.authenticated:
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.title("🔐 Login")
    st.markdown("---")
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if submit_button:
        if not username or not password:
            st.error("❌ Please enter both username and password.")
        else:
            try:
                user_data = conn.query(f"SELECT * FROM app_users WHERE username = '{username}' LIMIT 1;")
                if user_data.empty:
                    st.error("❌ Invalid username or password.")
                else:
                    user = user_data.iloc[0]
                    db_password_hash = user['password']
                    if bcrypt.checkpw(password.encode(), db_password_hash.encode()):
                        st.session_state.authenticated = True
                        st.session_state.user_username = username
                        payload = {
                            'username': username,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
                        }
                        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
                        st.session_state.jwt_token = token
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password.")
            except Exception as e:
                st.error(f"❌ Database error: {str(e)}")
    st.stop()

# ===================== Sidebar Navigation =====================
st.sidebar.title(f"👋 Hello, {st.session_state.user_username}")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Menu",
    ["Home", "Method Spend Analytics", "Source Spend Analytics"],
    index=["Home", "Method Spend Analytics", "Source Spend Analytics"].index(st.session_state.page),
    key="navigation"
)
st.session_state.page = page
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.user_username = None
    st.session_state.jwt_token = None
    st.session_state.page = "Home"
    st.rerun()
st.sidebar.markdown("---")

# st.markdown("### Your JWT Auth Token")
# st.code(st.session_state.jwt_token)

# ===================== Home Section =====================
if page == "Home":
    st.title("Expense Analytics")
    year_options = list(range(2024, pd.Timestamp.now().year + 1))
    selected_year = st.selectbox("Select Year", options=year_options, index=len(year_options)-1)
    data = conn.query(f"SELECT EXTRACT(MONTH FROM date) AS month_no,TRIM(TO_CHAR(date, 'Month')) AS month_name,ROUND(SUM(amount)::numeric, 2) AS total_amount FROM \"public\".\"expenses\" WHERE EXTRACT(YEAR FROM date) = {selected_year} AND is_deleted = 0 AND is_repayed = 0 GROUP BY TO_CHAR(date, 'Month'), EXTRACT(MONTH FROM date) ORDER BY EXTRACT(MONTH FROM date);")
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    data["month_name"] = pd.Categorical(data["month_name"], categories=month_order, ordered=True)
    st.bar_chart(data=data, x="month_name", y="total_amount", x_label="Month", y_label="Total Amount", sort=False)
    selected_month = st.selectbox("Select Month", options=month_order, index=month_order.index("January"))
    month_data = conn.query(f"SELECT EXTRACT(DAY FROM date) day_of_month,ROUND(SUM(amount)::numeric, 2) AS total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = {selected_year} AND EXTRACT(MONTH FROM date) = {month_order.index(selected_month)+1} AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(DAY FROM date) ORDER BY EXTRACT(DAY FROM date);")
    if not month_data.empty:
        st.line_chart(data=month_data, x="day_of_month", y="total_amount", x_label="Day of Month", y_label="Total Amount")
    else:
        st.write(f"No data available for {selected_month} {selected_year}.")

# ===================== Method Spend Analytics Section =====================
elif page == "Method Spend Analytics":
    st.title("Method Analytics")
    st.header("Spends Through All Methods in All Time")
    overall_spent_data = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT method_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE is_deleted = 0 AND is_repayed = 0 GROUP BY method_id)e LEFT JOIN payment_methods pm ON e.method_id = pm.id;")
    pie_chart_data = {
        "Method Name": overall_spent_data["method_name"],
        "Total Amount": overall_spent_data["total_amount"]
    }
    dataframe = pd.DataFrame(pie_chart_data)
    fig = px.pie(dataframe, values='Total Amount', names='Method Name', title='')
    st.plotly_chart(fig)
    st.markdown("---")
    year_options = list(range(2024, pd.Timestamp.now().year + 1))
    st.markdown("**<span style='font-size:1.5em'>Select Year</span>**", unsafe_allow_html=True)
    selected_year = st.selectbox("", options=year_options, index=len(year_options)-1, key="method_year")
    st.markdown("---")
    st.header(f"Spends Through All Methods In the Year {selected_year}")
    overall_spent_in_year_data = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT method_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY method_id)e LEFT JOIN payment_methods pm ON e.method_id = pm.id;")
    st.bar_chart(data=overall_spent_in_year_data, x="method_name", y="total_amount", x_label="Method Name", y_label="Total Amount", sort=False)
    st.markdown("---")
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    st.markdown("**<span style='font-size:1.5em'>Select Month</span>**", unsafe_allow_html=True)
    selected_month = st.selectbox("", options=month_order, index=month_order.index("January"), key="method_month")
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
    st.markdown("---")
    method_options = overall_spent_data['method_name'].unique()
    st.markdown("**<span style='font-size:1.5em'>Select Method</span>**", unsafe_allow_html=True)
    selected_method = st.selectbox("", options=method_options, key="selected_method")
    st.markdown("---")
    st.header(f"Spends Through {selected_method} in All Time")
    selected_method_id = overall_spent_data[overall_spent_data['method_name'] == selected_method]['method_id'].values[0]
    method_spends_over_years = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT EXTRACT(YEAR FROM date) cal_year, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE method_id = {selected_method_id} AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(YEAR FROM date))e LEFT JOIN payment_methods pm ON pm.id = {selected_method_id} ORDER BY cal_year;")
    st.line_chart(data=method_spends_over_years, x="cal_year", y="total_amount", x_label="Year", y_label="Total Amount")
    st.header(f"Overall Spends Through {selected_method}, over the months in the year {selected_year}")
    method_spends_over_months_in_year = conn.query(f"SELECT e.*, pm.name method_name FROM (SELECT EXTRACT(MONTH FROM date) cal_month, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE method_id = {selected_method_id} AND EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(MONTH FROM date))e LEFT JOIN payment_methods pm ON pm.id = {selected_method_id} ORDER BY cal_month;")
    st.bar_chart(data=method_spends_over_months_in_year, x="cal_month", y="total_amount", x_label="Month", y_label="Total Amount", sort=False)

# ===================== Source Spend Analytics Section =====================
elif page == "Source Spend Analytics":
    st.title("Source Analytics")
    st.header("Spends Through All Sources in All Time")
    overall_spent_data = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT source_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE is_deleted = 0 AND is_repayed = 0 GROUP BY source_id)e LEFT JOIN payment_sources ps ON e.source_id = ps.id;")
    pie_chart_data = {
        "Source Name": overall_spent_data["source_name"],
        "Total Amount": overall_spent_data["total_amount"]
    }
    dataframe = pd.DataFrame(pie_chart_data)
    fig = px.pie(dataframe, values='Total Amount', names='Source Name', title='')
    st.plotly_chart(fig)
    st.markdown("---")
    year_options = list(range(2024, pd.Timestamp.now().year + 1))
    st.markdown("**<span style='font-size:1.5em'>Select Year</span>**", unsafe_allow_html=True)
    selected_year = st.selectbox("", options=year_options, index=len(year_options)-1, key="source_year")
    st.markdown("---")
    st.header(f"Spends Through All Sources In the Year {selected_year}")
    overall_spent_in_year_data = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT source_id, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY source_id)e LEFT JOIN payment_sources ps ON e.source_id = ps.id;")
    st.bar_chart(data=overall_spent_in_year_data, x="source_name", y="total_amount", x_label="Source Name", y_label="Total Amount", sort=False)
    st.markdown("---")
    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    st.markdown("**<span style='font-size:1.5em'>Select Month</span>**", unsafe_allow_html=True)
    selected_month = st.selectbox("", options=month_order, index=month_order.index("January"), key="source_month")
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
    st.markdown("---")
    source_options = overall_spent_data['source_name'].unique()
    st.markdown("**<span style='font-size:1.5em'>Select Source</span>**", unsafe_allow_html=True)
    selected_source = st.selectbox("", options=source_options, key="selected_source")
    st.markdown("---")
    st.header(f"Spends Through {selected_source} in All Time")
    selected_source_id = overall_spent_data[overall_spent_data['source_name'] == selected_source]['source_id'].values[0]
    source_spends_over_years = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT EXTRACT(YEAR FROM date) cal_year, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE source_id = {selected_source_id} AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(YEAR FROM date))e LEFT JOIN payment_sources ps ON ps.id = {selected_source_id} ORDER BY cal_year;")
    st.line_chart(data=source_spends_over_years, x="cal_year", y="total_amount", x_label="Year", y_label="Total Amount")
    st.header(f"Overall Spends Through {selected_source}, over the months in the year {selected_year}")
    source_spends_over_months_in_year = conn.query(f"SELECT e.*, ps.name source_name FROM (SELECT EXTRACT(MONTH FROM date) cal_month, ROUND(SUM(amount)::numeric, 2) total_amount FROM expenses WHERE source_id = {selected_source_id} AND EXTRACT(YEAR FROM date) = '{selected_year}' AND is_deleted = 0 AND is_repayed = 0 GROUP BY EXTRACT(MONTH FROM date))e LEFT JOIN payment_sources ps ON ps.id = {selected_source_id} ORDER BY cal_month;")
    st.bar_chart(data=source_spends_over_months_in_year, x="cal_month", y="total_amount", x_label="Month", y_label="Total Amount", sort=False)
