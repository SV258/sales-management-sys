
import streamlit as st
import pandas as pd


def show_sql_engine(connection_factory):
        saved_queries = {
            "All Customer Sales":
               "SELECT * FROM customer_sales LIMIT 100;",

            "Overall Sales Summary":
               """SELECT COUNT(*) AS total_sales,
                      SUM(gross_sales) AS total_revenue,
                      SUM(received_amount) AS total_received
                 FROM customer_sales;""",

            "Branch-wise Sales":
               """SELECT branch_id,
                      COUNT(*) AS total_sales,
                      SUM(gross_sales) AS total_amount
                 FROM customer_sales
                 GROUP BY branch_id
                 ORDER BY branch_id;""",

            "Product-wise Sales":
               """SELECT product_name,
                      COUNT(*) AS total_sales,
                      SUM(gross_sales) AS total_revenue
                   FROM customer_sales
                   GROUP BY product_name
                   ORDER BY total_revenue DESC;""",

            "Payment Status":
                """SELECT status, COUNT(*) AS total_sales
                FROM customer_sales
                GROUP BY status;""",

            "Payment Splits":
                "SELECT * FROM payment_splits LIMIT 100;",

             "Custom SQL Query":
                "SELECT * FROM customer_sales LIMIT 10;"
        }

        selected_query = st.selectbox(
            "Select a saved SQL query",
            list(saved_queries.keys())
            )

        st.subheader("Advanced SQL Query Editor")

        query = st.text_area(
             "Enter your SELECT query",
             value=saved_queries[selected_query],
             height=150,
             key = selected_query
            )
        if  st.button("Execute SQL"):
            sql = query.strip()

            if not sql:
               st.warning("Please enter a SQL query.")
               return

        # Basic input checks, not a complete SQL security boundary.
            if not sql.upper().startswith("SELECT "):
               st.error("Only SELECT queries are allowed.")
               return

            connection = None
            cursor = None

            try:
               connection = connection_factory()
               cursor = connection.cursor()

               cursor.execute(sql)

               columns = [
                  column[0] for column in cursor.description
            ]

               rows = cursor.fetchall()
               df = pd.DataFrame(rows, columns=columns)

               st.success("Query executed successfully!")
               st.dataframe(df, use_container_width=True)

               csv = df.to_csv(index=False).encode("utf-8")

               st.download_button(
                "Download CSV",
                data=csv,
                file_name="sql_query_results.csv",
                mime="text/csv"
            )

            except Exception as error:
                st.error(f"SQL query failed: {error}")

            finally:
                if cursor is not None:
                   cursor.close()

                if connection is not None:
                   connection.close()
