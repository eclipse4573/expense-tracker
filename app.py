import streamlit as st
import pandas as pd
import os
from datetime import date
import login
import personalise
# from streamlit_option_menu import option_menu

st.set_page_config(page_title = "Expense Tracker", page_icon = "💰")

login.first_page()

selected = None
if login.st.session_state.logged_in:
    # st.toast("Logged in successfully!", icon = "✅")
    # st.toast(f"Welcome, {st.session_state.username}!", icon = "✅")
    with st.sidebar:
        # selected = option_menu("Main Menu", ["Add Expense", 'Expense History', 'Summary'], icons=['📈', '📜', '📊'], menu_icon="cast", default_index=1)
        # selected = st.radio(label = "Main Menu", options = ["Add/Delete Expense", 'Expense History', 'Summary'])
        st.sidebar.markdown("<h2 style='text-align:center;'>💰 Expense Tracker</h2>", unsafe_allow_html=True)
        st.sidebar.markdown("---")
        selected = st.radio(label = "Navigation 📌", options = ["Add/Delete Expense ➕", "Expense History 📜", "Summary 📊", "Personalise 🎯"])

file_path = f"expenses/{login.st.session_state.username}.csv"

if not os.path.exists(file_path):
    df = pd.DataFrame(columns = ["Date", "Category", "Amount", "Notes", "Payment Method"])
    df.to_csv(file_path, index = False)

def load_expenses():
    return pd.read_csv(file_path)

def save_expense(new_data):
    df = load_expenses()
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index = True)
    df.to_csv(file_path, index = False)

def delete_expense(delete_index):
    df = load_expenses()
    df = df.drop(index = delete_index)
    df.to_csv(file_path, index = False)
    st.toast("Expense deleted.", icon = "✅")

def logout_button():
    if st.button("Log Out"):
        login.st.session_state.logged_in = False
        login.st.session_state.username = None
        st.rerun()

if selected == "Add/Delete Expense ➕":
    st.subheader("Add/Delete Expense ➕")

    with st.form("new_expense", clear_on_submit = True):
        column1, column2, column3 = st.columns(3)
        with column1:
            expense_date = st.date_input("Date", date.today(), format = "DD/MM/YYYY")
        with column2:
            category = st.selectbox("Category", ["Food", "Shopping", "Utilities", "Transport", "Other"]) #update so user can add their own categories.
        with column3:
            amount = st.number_input("Amount", min_value = 0.0, format = "%.2f", step = 0.5) #only 2 decimal places will show.
        column4, column5 = st.columns(2)
        with column4:
            notes = st.text_input("Notes (optional)")
        with column5:
            payment_method = st.text_input("Payment Method") #update so user can add presaved methods.

        if st.form_submit_button("Add Expense"):
            save_expense({
                "Date": expense_date.strftime("%d-%m-%Y"),
                "Category": category,
                "Amount": amount,
                "Notes": notes,
                "Payment Method": payment_method
            })
            st.toast("Expense added!", icon = "✅")
    
    df = load_expenses()
    if len(df) > 0:
        with st.form("delete_expense", clear_on_submit = True):
            col1, col2 = st.columns([3, 1])  # wide table preview + narrow delete box
            with col1:
                st.dataframe(df.reset_index(drop=True), use_container_width=True)
            with col2:
                index = st.number_input(min_value = 0, max_value = (len(df) - 1), step = 1, label = "Which row would you like to delete?")
                if st.form_submit_button("Delete Expense"):
                    delete_expense(index)
                    st.rerun()
    
    logout_button()

elif selected == "Expense History 📜":
    st.subheader("Expense History 📜")
    df = load_expenses()

    df["Category"] = df["Category"].str.strip()
    category_filter = st.multiselect("Filter by Category", df["Category"].unique()) #.unique() just takes all the categories in the csv file and takes one instance of each.
    if category_filter:
        df = df[df["Category"].isin(category_filter)]

    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
    date_range = st.date_input("Filter by Date Range", [], format = "DD/MM/YYYY") #[] means no date selected.
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(pd.to_datetime(df["Date"]) >= pd.to_datetime(start_date)) & (pd.to_datetime(df["Date"]) <= pd.to_datetime(end_date))]

    st.dataframe(df, use_container_width = True)

    logout_button()

elif selected == "Summary 📊":
    st.subheader("Summary 📊")
    df = load_expenses()
    if not df.empty:
        total_spent = df["Amount"].sum()
        st.metric("Total Spent", f"₹{total_spent:,.2f}")
        st.bar_chart(df.groupby("Category")["Amount"].sum())
        df["Date"] = pd.to_datetime(df["Date"])
        daily_totals = df.groupby("Date")["Amount"].sum()
        st.line_chart(daily_totals)
    else:
        st.info("No expenses to display.")
    
    logout_button()

elif selected == "Personalise 🎯":
    personalise.customise()

#new vendor + nickname.
#upload and organise excel sheet.
#use ai for organisation (eventually).
