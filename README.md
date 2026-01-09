
# Spend Analyzer

Spend Analyzer is a Streamlit Single Page Web Application for visualizing and analyzing your expenses stored in a PostgreSQL database. It provides interactive charts to help you understand your monthly and daily spending patterns, with secure authentication and a unified navigation experience.

---

## Features

- **Secure Login & JWT Authentication:**
  - User authentication with hashed password validation (bcrypt).
  - JWT token generated and stored in session after login.
  - Only authenticated users can access analytics features.

- **Unified Navigation (Single-File App):**
  - All analytics and authentication logic are merged into a single file (`app.py`).
  - Custom sidebar navigation appears only after login.
  - No duplicate or public page links before authentication.

- **Yearly Expense Overview (Home Section):**
  - Select a year to view total expenses for each month.
  - Visualize monthly expenses using a bar chart.

- **Monthly Breakdown (Home Section):**
  - Select a month to see daily expense totals for that month.
  - Visualize daily expenses using a line chart.

- **Source Spend Analytics:**
  - View total spends through all payment sources for all time, a selected year, or a selected month.
  - Select a payment source to analyze its spending trends over the years and months.
  - Visualize spends by source using bar charts, line charts, and pie charts.

- **Method Spend Analytics:**
  - View total spends through all payment methods for all time, a selected year, or a selected month.
  - Select a payment method to analyze its spending trends over the years and months.
  - Visualize spends by method using bar charts, line charts, and pie charts.

- **Database Integration:**
  - Connects to a PostgreSQL database using `psycopg2` and SQLAlchemy.
  - Fetches and aggregates expense data dynamically based on user selections.

---

## How to Use

1. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   pip install streamlit
   ```

2. **Configure Database Connection**
   - Add your PostgreSQL connection details to `.streamlit/secrets.toml`:
     ```toml
     [connections.sql]
     url = "postgresql+psycopg2://<username>:<password>@<host>:<port>/<database>"
     ```

3. **Configure and Set JWT Secret (Optional but recommended)**
   - Add your JWT Secret details to `.streamlit/secrets.toml`:
   ```toml
     [auth]
     jwt_secret = "your jwt secret"
     ```

4. **Run the App**
   ```bash
   streamlit run app.py
   ```

5. **Navigate the App**
   - After login, use the sidebar to access Home, Method Spend Analytics, and Source Spend Analytics sections.
   - On the Home section, select the year and month to view overall and monthly expenses.
   - On the Source Spend Analytics section, analyze spends by payment source, year, and month with interactive charts.
   - On the Method Spend Analytics section, analyze spends by payment method, year, and month with interactive charts.

---

## File Structure

- `app.py` : Main Streamlit app containing authentication and all analytics logic
- `requirements.txt` : Python dependencies

---

## License

This project is licensed under the MIT License.
