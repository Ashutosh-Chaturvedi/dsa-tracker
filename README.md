# 🚀 DSA Problem Tracker API

A simple yet powerful backend API to track your Data Structures & Algorithms practice.
Built with **FastAPI + SQLite + SQLAlchemy**, this project helps you log, manage, and analyze your solved problems.

---

## 🔗 Live Demo

https://dsa-tracker-q4iy.onrender.com/docs

---

## 🧠 Features

*  Add solved problems
*  View all problems
*  Filter by difficulty and topic
*  Update problems (PUT & PATCH)
*  Persistent storage using SQLite
*  Clean API responses
*  Stats endpoint (counts by difficulty & platform)
*  Deployed and accessible online

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** SQLite
* **ORM:** SQLAlchemy
* **Validation:** Pydantic
* **Deployment:** Render

---

## 📂 Project Structure

```
dsa-tracker/
│
├── main.py          # API routes
├── models.py        # Database models
├── schemas.py       # Request/response schemas
├── database.py      # DB connection
├── crud.py          # (optional) DB logic
├── requirements.txt
└── start.sh
```

---

## 📌 API Endpoints

### 🔹 Health Check

```
GET /
```

---

### 🔹 Add Problem

```
POST /problems
```

---

### 🔹 Get All Problems

```
GET /problems
```

#### With filters:

```
GET /problems?difficulty=Easy
GET /problems?topic=Array
```

---

### 🔹 Get Problem by ID

```
GET /problems/{id}
```

---

### 🔹 Update Problem (Full)

```
PUT /problems/{id}
```

---

### 🔹 Update Problem (Partial)

```
PATCH /problems/{id}
```

---

### 🔹 Stats

```
GET /stats
```

Returns:

* total problems
* count by difficulty
* count by platform

---

## 📊 Example Response

```json
{
  "status": "success",
  "data": {
    "total": 50,
    "difficulty": {
      "easy": 20,
      "medium": 20,
      "hard": 10
    },
    "platform": {
      "leetcode": 30,
      "hackerrank": 10,
      "other": 10
    }
  }
}
```

---

## ⚙️ Setup Locally

### 1. Clone repo

```
git clone <your-repo-url>
cd dsa-tracker
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run server

```
uvicorn main:app --reload
```

### 5. Open Swagger

```
http://127.0.0.1:8000/docs
```

---

##  Future Improvements

* PostgreSQL integration
* Authentication (JWT)
* Date-based filtering
* Topic analytics
* Frontend dashboard

---

##  What I Learned

* Designing REST APIs
* Using SQLAlchemy ORM
* Handling database queries efficiently
* API response structuring
* Deployment and debugging
* Real-world backend development workflow

---

##  Conclusion

This project demonstrates the ability to build, structure, and deploy a complete backend service with real-world features.

---

⭐ If you like this project, consider giving it a star!
