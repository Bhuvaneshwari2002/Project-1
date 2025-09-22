# Project-1
📌**CLIENT QUERY MANAGEMENT SYSTEM**

📖Overview:
Client Query Management System is a simple web application built using Streamlit where:

- Clients can login & raise their queries.
- Support team members can login and view all queries,close open queries.


🚀Features:
- Client Login & Query Submission – Secure login and easy to use form for raising queries.
- Support Dashboard – View open and closed queries,view the history of closed queries.
- Query Tracking – Track query status (Open/Closed) with timestamps.
- Streamlit UI - Interactive interface for both clients & support team members.


🛠 Tech Stack:
- Frontend / App: Python, Streamlit
- Database: MySQL
- Libraries:-
   - pymysql.
   - hashlib.
   - pandas, numpy.

⚙️ Setup Instructions:

1️⃣ Download the Project:

    git clone https://github.com/Bhuvaneshwari2002/client-query-system.git
    cd client-query-system

2️⃣ Install Packages:
Create a virtual environment and install required packages:

    pip install streamlit pymysql pandas numpy

3️⃣ Setup MySQL Database:
Open MySql & run:

    SOURCE database/Client Query Management System (DB).sql;

4️⃣ Run the Streamlit app:

    streamlit run app.py
    

📸Sreenshots for reference:
✅Login Page:
<img width="1920" height="916" alt="image" src="https://github.com/user-attachments/assets/fe8bf401-f8c9-4779-85df-6d25bc941c9b" />

✅Client Page:
<img width="1920" height="931" alt="Client_page" src="https://github.com/user-attachments/assets/627b733e-78ab-4f56-98be-8fdc6574cd32" />

✅Support Page:
<img width="1920" height="921" alt="Support_page" src="https://github.com/user-attachments/assets/1eb5f439-f492-470c-a278-97caf39c2e61" />

✅Analytics:
  - Pie chart of open vs closed queries:
<img width="1920" height="912" alt="Analytics chart" src="https://github.com/user-attachments/assets/0ea18437-c410-4bca-8080-c20d29cd7dbb" />

  - Barplot of common queries:
<img width="1920" height="911" alt="Barplot" src="https://github.com/user-attachments/assets/72c301d4-c8d7-4382-96d2-1382facbdc1c" />










