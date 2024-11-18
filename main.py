import pandas as pd
import csv
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

# Constants
CSV_FILE = "finance_data.csv"
COLUMNS = ["date", "amount", "category", "description"]
FORMAT = "%d-%m-%Y"

# Initialize the CSV file if not present
def initialize_csv():
    try:
        pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)

# Add a new entry
def add_entry(date, amount, category, description):
    new_entry = {
        "date": date,
        "amount": amount,
        "category": category,
        "description": description,
    }
    with open(CSV_FILE, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
        writer.writerow(new_entry)

# Get transactions within a date range
def get_transactions(start_date, end_date):
    df = pd.read_csv(CSV_FILE)
    df["date"] = pd.to_datetime(df["date"], format=FORMAT)
    start_date = datetime.strptime(start_date, FORMAT)
    end_date = datetime.strptime(end_date, FORMAT)

    mask = (df["date"] >= start_date) & (df["date"] <= end_date)
    filtered_df = df.loc[mask]
    return filtered_df

# Plot transactions
def plot_transactions(df):
    df["date"] = pd.to_datetime(df["date"], format=FORMAT)
    df.set_index("date", inplace=True)

    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)

# Streamlit App
def main():
    st.title("Personal Finance Tracker")
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Add Transaction", "View Transactions", "About"])

    initialize_csv()

    if page == "Add Transaction":
        st.header("Add a New Transaction")
        date = st.date_input("Date", value=datetime.now()).strftime(FORMAT)
        amount = st.number_input("Amount", min_value=0.01, format="%.2f")
        category = st.selectbox("Category", ["Income", "Expense"])
        description = st.text_input("Description (optional)")

        if st.button("Add Transaction"):
            add_entry(date, amount, category, description)
            st.success("Transaction added successfully!")

    elif page == "View Transactions":
        st.header("View Transactions and Summary")
        start_date = st.date_input("Start Date", value=datetime.now()).strftime(FORMAT)
        end_date = st.date_input("End Date", value=datetime.now()).strftime(FORMAT)

        if st.button("Show Transactions"):
            df = get_transactions(start_date, end_date)
            if df.empty:
                st.warning("No transactions found in the given date range.")
            else:
                st.subheader("Transactions")
                st.write(df)

                total_income = df[df["category"] == "Income"]["amount"].sum()
                total_expense = df[df["category"] == "Expense"]["amount"].sum()
                st.subheader("Summary")
                st.write(f"**Total Income:** ${total_income:.2f}")
                st.write(f"**Total Expense:** ${total_expense:.2f}")
                st.write(f"**Net Savings:** ${total_income - total_expense:.2f}")

                if st.button("Show Plot"):
                    plot_transactions(df)

    elif page == "About":
        st.header("About This App")
        st.write("This is a simple personal finance tracker built with Streamlit.")

if __name__ == "__main__":
    main()