import streamlit as st
import pandas as pd
import pymysql
import hashlib

st.title("Client Query Management System")

# ==========================
# CONFIGURATION
# ==========================
USE_DATABASE = False  # ❌ Change to True after you set up a cloud DB

DB_CONFIG = {
    "host": "localhost",   # e.g. Railway or PlanetScale host
    "user": "root",
    "password": "123456789",
    "database": "client_query"
}

# ==========================
# UTILITIES
# ==========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_connection():
    if not USE_DATABASE:
        return None
    return pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# ==========================
# AUTHENTICATION
# ==========================
def login_user(username, password, role):
    if not USE_DATABASE:
        # Fake login for testing
        if username == "test" and password == "123":
            return {"username": "test", "role": role}
        return None
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND hashed_password=%s AND role=%s",
            (username, hash_password(password), role)
        )
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        st.error(f"❌ DB Error: {e}")
        return None

def login_page():
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.sidebar.radio("Select role", ("client", "support"))

    if st.button("Login"):
        user = login_user(username, password, role)
        if user:
            st.success(f"✅ Welcome {username} ({role})!")
            st.session_state.page = role
        else:
            st.error("❌ Invalid username or password")

# ==========================
# CLIENT DASHBOARD
# ==========================
def client_page():
    st.subheader("Submit a Query")
    email = st.text_input("Email ID*")
    mobile = st.text_input("Mobile Number*")
    heading = st.text_input("Query Heading*")
    description = st.text_area("Query Description*")

    if st.button("Submit Query"):
        if not email or not mobile or not heading or not description:
            st.warning("⚠ Please fill all required fields")
        else:
            if not USE_DATABASE:
                st.success("✅ Query submitted (testing mode, not saved).")
                return
            try:
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
            except Exception as e:
                st.error(f"❌ DB Error: {e}")

# ==========================
# SUPPORT DASHBOARD
# ==========================
def support_page():
    st.subheader("Support Dashboard")
    filter_option = st.selectbox("Filter by status", ["All", "Opened", "Closed"])

    if not USE_DATABASE:
        st.info("📌 Testing mode: Showing sample data")
        sample_data = pd.DataFrame([
            {"query_id": 1, "client_email": "abc@test.com", "query_heading": "Login Issue",
             "query_description": "Unable to login", "status": "Opened", "date_raised": "2025-09-22"}
        ])
        st.dataframe(sample_data)
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        if filter_option == "All":
            cursor.execute("""
                SELECT query_id, client_email, query_heading, query_description, status, date_raised, date_closed
                FROM client ORDER BY date_raised DESC
            """)
        else:
            cursor.execute("""
                SELECT query_id, client_email, query_heading, query_description, status, date_raised, date_closed
                FROM client WHERE status=%s ORDER BY date_raised DESC
            """, (filter_option,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            st.info(f"No {filter_option.lower()} queries found.")
            return

        for row in rows:
            with st.expander(f"#{row['query_id']} - {row['query_heading']} ({row['status']})"):
                st.write(f"*Email:* {row['client_email']}")
                st.write(f"*Description:* {row['query_description']}")
                st.write(f"*Status:* {row['status']}")
                st.write(f"*Raised On:* {row['date_raised']}")

                if row["status"] == "Closed" and row["date_closed"]:
                    st.write(f"*Closed On:* {row['date_closed']}")

                if row["status"] == "Opened":
                    if st.button(f"Close Query {row['query_id']}", key=f"close_{row['query_id']}"):
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                "UPDATE client SET status='Closed', date_closed=NOW() WHERE query_id=%s",
                                (row["query_id"],)
                            )
                            conn.commit()
                            conn.close()
                            st.success(f"✅ Query {row['query_id']} closed successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ DB Error: {e}")
    except Exception as e:
        st.error(f"❌ DB Error: {e}")

# ==========================
# NAVIGATION
# ==========================
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
