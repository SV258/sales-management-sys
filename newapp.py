import streamlit as st
import mysql.connector
import bcrypt
import pandas as pd
from sql_engine import show_sql_engine
from sql_connection import get_sql_connection


st.set_page_config(page_title="Sales Management System", layout="wide")


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=st.secrets["mysql_password"],
        database="sales_management_sys"
    )

def show_admin_sales_report(branch_id):
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM customer_sales WHERE branch_id = %s",
                (branch_id,)
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()

    branch_names = {1:"Chennai",2:"Bangalore",3:"Hyderabad",4:"Delhi",5:"Mumbai",6:"pune",7:"Kolkata",8:"Ahmedabad"}
    branch_name = branch_names.get(int(branch_id),"Unknown Branch")
    st.subheader(f"{branch_name}Branch-Customer Sales Report")

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No sales found for your branch.")

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

def show_financial_summary(branch, product, start_date, end_date):
    branch_ids = {
        "Chennai": 1,
        "Bangalore": 2,
        "Hyderabad": 3,
        "Delhi": 4,
        "Mumbai": 5,
        "Pune": 6,
        "Kolkata": 7,
        "Ahmedabad": 8
    }

    query = """
        SELECT
            COALESCE(SUM(gross_sales), 0) AS total_revenue,
            COALESCE(SUM(received_amount), 0) AS total_received,
            COALESCE(SUM(pendind_amount), 0) AS total_pending
        FROM customer_sales
        WHERE 1 = 1
    """

    params = []

    if branch != "All":
        query += " AND branch_id = %s"
        params.append(branch_ids[branch])

    if product != "All":
        query += " AND product_name = %s"
        params.append(product)

    if start_date is not None:
        query += " AND date >= %s"
        params.append(start_date)

    if end_date is not None:
        query += " AND date <= %s"
        params.append(end_date)

    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query, tuple(params))
            result = cursor.fetchone()
        finally:
            cursor.close()
    finally:
        connection.close()

    revenue = float(result["total_revenue"])
    received = float(result["total_received"])
    pending = float(result["total_pending"])

    pending_pct = (
        (pending / revenue) * 100 if revenue > 0 else 0
    )

    st.subheader("💵 Financial Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Revenue (Gross)", f"₹{revenue:,.2f}")

    with col2:
        st.metric("Total Received Amount", f"₹{received:,.2f}")

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Total Pending Amount", f"₹{pending:,.2f}")

    with col4:
        st.metric("Pending Collection %", f"{pending_pct:.2f}%")


def show_super_admin_filters():
    st.subheader("🔍 Filter Controls")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        branch = st.selectbox(
            "Branch Name",
            ["All", "Chennai", "Bangalore", "Hyderabad",
             "Delhi", "Mumbai", "Pune", "Kolkata", "Ahmedabad"]
        )
    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT DISTINCT product_name
                FROM customer_sales
                WHERE product_name IS NOT NULL
                  AND product_name != ''
                ORDER BY product_name
            """)
            products = [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
    finally:
        connection.close()

    with col2:
        product = st.selectbox(
            "Product Name",
            ["All"] + products
        )

    with col3:
        start_date = st.date_input("Start Date", value=None)

    with col4:
        end_date = st.date_input("End Date", value=None)

    return branch, product, start_date, end_date

st.title("Sales Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Sales Management System Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            connection = get_connection()
            try:
                cursor = connection.cursor()
                try:
                    cursor.execute(
                        "SELECT password, role,branch_id FROM users WHERE username = %s",
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
                st.session_state.branch_id =user[2]
                st.rerun()
            else:
                st.error("Invalid username or password")
        except mysql.connector.Error as error:
            st.error(f"Database error: {error}")
        except (ValueError, TypeError) as error:
            st.error(f"Password verification error: {error}")

else:
    if "role" not in st.session_state:
        st.session_state.role = None
    st.success("Login successful!")
    st.write("Welcome:", st.session_state.username)
    st.write("Role:", st.session_state.role)
    with st.sidebar:
        st.title("Navigation")

        page = st.radio(
            "Go to",
            [
            "Dashboard & Reports",
            "Record Creator",
            "Advanced SQL Engine"
            ]
       )
    if st.session_state.role.lower().replace("_", " ") == "super admin":
        if page == "Dashboard & Reports":
            st.header("Super Admin Dashboard")

            try:
                show_customer_sales_report()
            except mysql.connector.Error as error:
                st.error(f"Could Not Load Customer Sales Report: {error}")

        elif page == "Record Creator":
            st.header("Record Creator")
            branch, product, start_date, end_date = show_super_admin_filters()
            show_financial_summary(branch, product, start_date, end_date)
            st.divider()
            show_new_sales_form()
            st.divider()
            st.subheader("Payment Entry Form")
            show_payment_entry_form()
        elif page == "Advanced SQL Engine":
            st.header("Advanced SQL Engine")
            show_sql_engine(get_sql_connection)
    elif st.session_state.role.lower().strip() == "admin":
        if page == "Dashboard & Reports":
            st.header("Admin Dashboard")

            branch_id = st.session_state.branch_id

            if branch_id is not None:
                st.success("Admin Login Successful")
                st.write("Welcome:", st.session_state.username)
                st.write("Your branch ID:", branch_id)
                show_admin_sales_report(branch_id)
            else:
                st.warning("No branch assigned to this admin.")

        elif page == "Record Creator":
            st.header("Record Creator")
            st.info("Branch Admin operations will be added here.")

        elif page == "Advanced SQL Engine":
            st.header("Advanced SQL Engine")
            st.warning("This feature is restricted to Super Admin.")
    else:
            st.error("AccessDenied:invalid user role.")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
