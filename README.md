# Spend Analyzer

Spend Analyzer is a Streamlit web application for visualizing and analyzing your expenses stored in a PostgreSQL database. It provides interactive charts to help you understand your monthly and daily spending patterns.


## Features

- **Yearly Expense Overview (Home Page):**
  - Select a year to view total expenses for each month.
  - Visualize monthly expenses using a bar chart.

- **Monthly Breakdown (Home Page):**
  - Select a month to see daily expense totals for that month.
  - Visualize daily expenses using a line chart.

- **Source Spend Analytics (Source Data Page):**
  - View total spends through all payment sources for all time, a selected year, or a selected month.
  - Select a payment source to analyze its spending trends over the years and months.
  - Visualize spends by source using bar charts and line charts.
  - Interactive dropdowns for year, month, and source selection with bold, large labels for clarity.

- **Database Integration:**
  - Connects to a PostgreSQL database using `psycopg2` and SQLAlchemy.
  - Fetches and aggregates expense data dynamically based on user selections.

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

3. **Run the App**
   ```bash
   streamlit run home.py
   ```

4. **Navigate the App**
  - Use the sidebar to access the Home page and Source Spend Analytics page.
  - On the Home page, select the year and month to view overall and monthly expenses.
  - On the Source Spend Analytics page, analyze spends by payment source, year, and month with interactive charts.

## File Structure

- `home.py` : Main Streamlit app for expense analysis
- `pages/Source Spend Analytics.py` : Analyze spends by payment source, year, and month
- `pages/` : Additional analytics pages (if any)
- `requirements.txt` : Python dependencies

## License

This project is licensed under the MIT License.
