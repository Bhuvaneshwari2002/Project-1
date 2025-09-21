import pymysql
import streamlit as st
import pandas as pd
import numpy as np 
import hashlib

st.title("Client Query Management System")

#hashing password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#connecting DB
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",            
        password="123456789",
        database="client_query",
        cursorclass=pymysql.cursors.DictCursor
    )

#login page
def login_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND hashed_password=%s AND role=%s",
        (username, hash_password(password), role)
    )
    result = cursor.fetchone()
    conn.close()
    return result

def login_page():
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.sidebar.radio('select any one',("client", "support")) 

    if st.button("Login"):
        user = login_user(username, password, role)
        if user:
            st.success(f"✅Welcome! You are logged in.")
            if role == "client":
                st.session_state.page = "client"
            else:
                st.session_state.page = "support"
        else:
            st.error("❌ Invalid username or password")


#client dashboard 
def client_page():
    st.subheader("Submit a Query")
    email = st.text_input("Email ID*")
    mobile = st.text_input("Mobile Number*")
    heading = st.text_input("Query Heading*")
    description = st.text_area("Query Description*")

    if st.button("Submit Query"):
        if not email or not mobile or not heading or not description:
            st.warning("⚠️ Please fill all the required * fields.")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO client (client_email, client_mobile, query_heading, query_description, status, date_raised) 
                VALUES (%s, %s, %s, %s, %s, NOW())
                """,
                (email, mobile, heading, description, "Opened")
            )
            conn.commit()
            conn.close()
            st.success("✅ Your query has been submitted successfully!")


#support dashboard
def support_page():
    st.subheader("Support Dashboard")

    #To filter query status
    filter_option = st.selectbox(
        "Filter by status",
        ["All", "Opened", "Closed"]
    )

    conn = get_connection()
    cursor = conn.cursor()

    #To apply status filter option in SQL query
    if filter_option == "All":
        cursor.execute("""
            SELECT query_id, client_email, query_heading, query_description, status, date_raised, date_closed
            FROM client
            ORDER BY date_raised DESC
        """)
    else:
        cursor.execute("""
            SELECT query_id, client_email, query_heading, query_description, status, date_raised, date_closed
            FROM client
            WHERE status=%s
            ORDER BY date_raised DESC
        """, (filter_option,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        st.info(f"No {filter_option.lower()} queries found.")
        return

    #To display queries
    for row in rows:
        query_id = row["query_id"]
        email = row["client_email"]
        heading = row["query_heading"]
        description = row["query_description"]
        status = row["status"]
        date_raised = row["date_raised"]
        date_closed = row["date_closed"]

        with st.expander(f"#{query_id} - {heading} ({status})"):
            st.write(f"**Email:** {email}")
            st.write(f"**Description:** {description}")
            st.write(f"**Status:** {status}")
            st.write(f"**Raised On:** {date_raised}")

            if status == "Closed" and date_closed:
                st.write(f"**Closed On:** {date_closed}")

            # ✅ Show button ONLY for open queries
            if status == "Opened":
                if st.button(f"Close Query {query_id}", key=f"close_{query_id}"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE client SET status='Closed', date_closed=NOW() WHERE query_id=%s",
                        (query_id,)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Query {query_id} closed successfully!")
                    st.rerun()

if "page" not in st.session_state:
    st.session_state.page = "login"
if st.sidebar.button("Logout"):
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "client":
    client_page()
elif st.session_state.page == "support":
    support_page()
