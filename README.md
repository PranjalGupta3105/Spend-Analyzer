# Spend Analyzer

Spend Analyzer is a Streamlit web application for visualizing and analyzing your expenses stored in a PostgreSQL database. It provides interactive charts to help you understand your monthly and daily spending patterns.

## Features

- **Yearly Expense Overview:**
  - Select a year to view total expenses for each month.
  - Visualize monthly expenses using a bar chart.

- **Monthly Breakdown:**
  - Select a month to see daily expense totals for that month.
  - Visualize daily expenses using a line chart.

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
   - Use the sidebar to select the year and month.
   - View interactive charts for your expenses.

## File Structure

- `home.py` : Main Streamlit app for expense analysis
- `pages/` : Additional analytics pages (if any)
- `requirements.txt` : Python dependencies

## License

This project is licensed under the MIT License.
