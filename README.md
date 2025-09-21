# Project-1
📌**CLIENT QUERY MANAGEMENT SYSTEM**

📖Overview:
Client Query Management System is a simple web application built using Streamlit where:

- clients can login & raise their queries
- support team members can login and view all queries,close open queries and can see the history of closed queries


🚀Features:
- Client Login & Query Submission – Secure login and easy to use form for raising queries.
- Support Dashboard – View open and closed queries,view the history of closed queries.
- Query Tracking – Track query status (Open/Closed) with timestamps.
- Streamlit UI - Clean,interactive interface for both clients & support team members


🛠 Tech Stack:
- Frontend / App: Python, Streamlit
- Database: MySQL
📚Libraries:-

   - pymysql
   - hashlib
   - pandas, numpy

⚙️ Setup Instructions

1️⃣ Download the Project:

    git clone https://github.com/your-username/client-query-system.git
    cd client-query-system

2️⃣ Install Dependencies:
Create a virtual environment and install required packages:

    pip install streamlit pymysql pandas numpy

3️⃣ Setup MySQL Database:
Open MySql & run:

    SOURCE database/Client Query Management System (DB).sql;

4️⃣ Run the Streamlit app:

    streamlit run app.py




