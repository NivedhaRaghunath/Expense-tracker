import streamlit as st
from  streamlit_gsheets import GSheetsConnection
import pandas as pd

# title and description

st.title("Expenses Management Portal")
st.markdown("Enter the details of Expenses")

# Establish the gsheet connections
conn = st.connection("gsheets",type = GSheetsConnection)

# Fetch existing expense data
existing_data = conn.read(worksheet="expenses",usecols=list(range(5)),ttl=5)
existing_data = existing_data.dropna(how="all")

#st.dataframe(existing_data)
#List of expenses

EXPENSES = ["Grocery","House_Hold","Fuel","Repair","Snacks","Pooja-Items"]
MODE = ["Cash","Card","UPI"]

with st.form(key = "expenses_form"):
    date = st.date_input(label="Select the date*")
    expense_name = st.selectbox("Nature of Expense*",options=EXPENSES,index=None)
    amount = st.number_input(label="Enter the amount*")
    mode = st.selectbox("Select the mode of payment",options=MODE)
    remarks = st.text_area(label="Remarks")

    st.markdown("**required")

    submit_button = st.form_submit_button(f"Submit the expenses for the date {date}")

    if submit_button:
        if not date or not expense_name or not amount:
            st.warning("Please fill all the mandatory fields")
            st.stop()
        else:
            expense_dict = [
                    {"DATE" : date,
                     "EXPENSE TYPE" : expense_name,
                     "AMOUNT" : amount,
                     "MODE OF PAYMENT" : mode,
                     "REMARKS" : remarks
                     }
                ]
            
            expense_df = pd.DataFrame(expense_dict)
        

            # Add the new expense to the existing expense

            updated_df = pd.concat( [existing_data,expense_df],ignore_index=True)

            # update google sheets with the new expense data

            conn.update(worksheet="expenses",data=updated_df)
            st.success("Expenses are updated succesfully")

    



