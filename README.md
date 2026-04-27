# AIQuest FastAPI Course Management API

A professional FastAPI application for managing course data, built with a modular structure and SQLAlchemy ORM.

## 🚀 Features
- **FastAPI**: High-performance web framework.
- **SQLAlchemy ORM**: Professional database interaction.
- **PostgreSQL**: Robust relational database support.
- **Modular Structure**: Clean separation of concerns (Models, Schemas, CRUD, Routers).
- **Auto-Docs**: Interactive Swagger documentation.

## 📁 Project Structure
```text
fastapi/
├── app/
│   ├── main.py          # App initialization & router inclusion
│   ├── database.py      # SQLAlchemy engine & session setup
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic models (Data validation)
│   ├── crud.py          # Database CRUD logic
│   └── routers/
│       └── courses.py    # Course-specific API endpoints
├── requirements.txt      # Project dependencies
└── .gitignore            # Git ignore file
```

## 🛠️ Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd fastapi
```

### 2. Set up Virtual Environment
```powershell
# Create venv
python -m venv env

# Activate venv (Windows)
.\env\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Database Configuration
Ensure you have a PostgreSQL database running. Update the `SQLALCHEMY_DATABASE_URL` in `app/database.py` with your credentials:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:port/database"
```

## 🏃 Running the Application
Start the development server using uvicorn:
```powershell
uvicorn app.main:app --reload
```

## 📖 API Documentation
Once the server is running, you can access the interactive documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🛣️ API Endpoints
- `GET /`: Welcome message.
- `GET /about`: About the API.
- `GET /courses/`: List all courses.
- `POST /courses/`: Create a new course.
- `GET /courses/{id}`: Get course details by ID.
- `PATCH /courses/{id}`: Update a course.
- `DELETE /courses/{id}`: Delete a course.
