import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Your Google Sheet Name").worksheet("expenses")

# Fetch existing expense data
existing_data = pd.DataFrame(sheet.get_all_records())

st.title("Expenses Management Portal")
st.markdown("Enter the details of Expenses")

EXPENSES = ["Grocery","House_Hold","Fuel","Repair","Snacks","Pooja-Items"]
MODE = ["Cash","Card","UPI"]

with st.form(key="expenses_form"):
    date = st.date_input(label="Select the date*")
    expense_name = st.selectbox("Nature of Expense*", options=EXPENSES, index=None)
    amount = st.number_input(label="Enter the amount*")
    mode = st.selectbox("Select the mode of payment", options=MODE)
    remarks = st.text_area(label="Remarks")

    st.markdown("**required")

    submit_button = st.form_submit_button(f"Submit the expenses for the date {date}")

    if submit_button:
        if not date or not expense_name or not amount:
            st.warning("Please fill all the mandatory fields")
            st.stop()
        else:
            expense_dict = [
                {"DATE": date,
                 "EXPENSE TYPE": expense_name,
                 "AMOUNT": amount,
                 "MODE OF PAYMENT": mode,
                 "REMARKS": remarks
                 }
            ]
            
            expense_df = pd.DataFrame(expense_dict)

            # Add the new expense to the existing expense
            updated_df = pd.concat([existing_data, expense_df], ignore_index=True)

            # Update Google Sheets with the new expense data
            sheet.append_rows(expense_df.values.tolist())
            st.success("Expenses are updated successfully")
