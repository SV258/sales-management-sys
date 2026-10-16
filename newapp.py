import streamlit as st
import mysql.connector
import bcrypt
import pandas as pd

st.set_page_config(page_title="Sales Management System", layout="wide")


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=st.secrets["mysql_password"],
        database="sales_management_sys"
    )


def show_customer_sales_report():
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM customer_sales")
            rows = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()

    st.subheader("Customer Sales Report")
    if rows:
        df = pd.DataFrame(rows)
        st.write("### filter customer sales")
        branches=sorted(df["branch_id"].dropna().unique().tolist())
        selected_branch=st.selectbox("Select Branch",["All"]+branches,format_func=str
        )

        products=sorted(df["product_name"].dropna().unique().tolist())
        selected_product=st.selectbox("Select Product",["All"]+products
        )

        df["date"]=pd.to_datetime(df["date"])
        start_date=st.date_input("start Date",value=df["date"].min().date()
        )

        end_date=st.date_input("End Date",value=df["date"].max().date()
        )

        filtered_df=df.copy()
        if selected_branch!="All":
            filtered_df=filtered_df[filtered_df["branch_id"]==selected_branch]
        if selected_product!="All":
            filtered_df=filtered_df[filtered_df["product_name"]==selected_product]
        if start_date>end_date:
            st.warning("start date must be before end date")
        else:
            filtered_df=filtered_df[(filtered_df["date"].dt.date>=start_date)&
            (filtered_df["date"].dt.date<=end_date)]
        st.dataframe(filtered_df,use_container_width=True)
        st.write("Total Records:",len(filtered_df))
    else:
        st.info("The customer_sales table is empty.")

def show_new_sales_form():
    st.subheader("New Sales Entry")

    with st.form("new_sales_form"):
        branch_id = st.number_input("Branch ID",min_value=1,step=1)
        sale_date = st.date_input("Sale Date")
        name = st.text_input("Customer Name")
        mobile_number = st.text_input("Mobile Number")
        product_name = st.text_input("Product Name")
        gross_sales = st.number_input("Gross Sales Amount",min_value=0.01,step=100.0)
        submitted = st.form_submit_button("Save Sale")
    if submitted:
        if not name.strip() or not product_name.strip():
            st.error("please enter customer name and product.")
            return
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query ="""insert into customer_sales(branch_id,date,name,mobile_number,product_name,gross_sales,received_amount,pendind_amount,status)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            values = (int(branch_id),sale_date,name.strip(),mobile_number.strip(),product_name.strip(),gross_sales,0,gross_sales,"open")
            cursor.execute(query,values)
            connection.commit()
            st.success("Sale saved successfully.")
        except mysql.connector.Error as error:
            if connection is not None:
                connection.rollback()
            st.error(f"Database error: {error}")
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
def show_payment_entry_form():
    st.subheader("payment Entry")
    with st.form("payment_entry_form"):
        sale_id =st.number_input("sale ID",min_value=1,step=1)
        payment_date = st.date_input("Payment Date")
        amount_paid = st.number_input("Amount Paid",min_value=0.01,step=100.0)
        payment_method = st.selectbox("Payment Method", ["Cash", "Card", "Bank Transfer", "UPI"])
        submitted = st.form_submit_button("Save Payment")
    if submitted:
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            query ="""insert into payment_splits(sale_id,payment_date,amount_paid,payment_method)values(%s,%s,%s,%s)"""
            values = (int(sale_id),payment_date,amount_paid,payment_method)
            cursor.execute(query,values)
            connection.commit()
            st.success("Payment saved successfully.")
        except mysql.connector.Error as error:
            if connection is not None:
                connection.rollback()
            st.error(f"Database error: {error}")
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

st.title("Sales Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Super Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            connection = get_connection()
            try:
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        "SELECT password, role FROM users WHERE username = %s",
                        (username,)
                    )
                    user = cursor.fetchone()
                finally:
                    cursor.close()
            finally:
                connection.close()

            if user and bcrypt.checkpw(
                password.encode("utf-8"),
                user[0].encode("utf-8") if isinstance(user[0], str) else user[0]
            ):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = str(user[1]).strip()
                st.rerun()
            else:
                st.error("Invalid username or password")
        except mysql.connector.Error as error:
            st.error(f"Database error: {error}")
        except (ValueError, TypeError) as error:
            st.error(f"Password verification error: {error}")

else:
    st.success("Login successful!")
    st.write("Welcome:", st.session_state.username)
    st.write("Role:", st.session_state.role)

    if st.session_state.role.lower().replace("_", " ") == "super admin":
        st.header("Super Admin Dashboard")
        try:
            show_customer_sales_report()
        except mysql.connector.Error as error:
            st.error(f"Could not load Customer Sales Report: {error}")
        st.divider()
        show_new_sales_form()
        st.divider()
        show_payment_entry_form()

    else:
        st.warning("Only Super Admin can view the Customer Sales Report.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
