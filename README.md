README.md
🧮 Frontend-Backend Separation Calculator - Backend Service
Project Introduction: A calculator backend service built with Flask and SQLite. It provides complete interfaces for expression calculation, data persistence, historical record pagination, keyword search, and single/batch record deletion, delivering stable data support for the frontend calculator page.

---
📌 Tech Stack
- Backend Framework: Flask
- Database: SQLite (lightweight, zero-configuration, persistent storage)
- ORM: Flask-SQLAlchemy
- Cross-domain Handling: Flask-CORS

---
✨ Core Features
- Supports basic four arithmetic operations and compound operations with parentheses
- Automatically rounds calculation results to 6 decimal places to avoid messy layout caused by ultra-long decimals
- All calculation records are persistently stored in the database, and data will not be lost after service restart
- Automatically converts time to Beijing Time (UTC+8)
- Paginated display of historical records to prevent unlimited page scrolling
- Fuzzy search supported for calculation expressions and results
- Supports deleting a single historical record and clearing all records in one click
- Complete cross-domain support for frontend-backend separated deployment

---
📡 API Documentation
1. Submit Calculation (POST)
/api/calculate
Function: Receive mathematical expressions from the frontend, execute calculation, and store records in the database.
2. Get Paginated History Records (GET)
/api/history?page=1&size=5&keyword=
Function: Query records by page and support keyword search for expressions or results.
3. Delete Single History Record (DELETE)
/api/history/<id>
4. Clear All History Records (DELETE)
/api/history

---
💻 Local Deployment Guide
1. Install Dependencies
pip install flask flask-sqlalchemy flask-cors
2. Start Backend Service
python main.py
3. Service Address
Default running address: http://127.0.0.1:5000

---
📁 Project Structure
calculator_backend/
├── instance/
│   └── calculator.db   # SQLite persistent database file
├── main.py            # Main program, API interfaces and database models
└── README.md          # Project documentation

---
🎯 Project Advantages
- Automatic database and table creation on service startup (no manual configuration required)
- Fixed absolute database path to avoid data confusion and loss
- Unified precision processing for clean and standardized historical record display
- Standard API design with clear logic, fully meeting frontend-backend separation course assignment requirements
