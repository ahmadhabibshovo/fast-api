import time
import psycopg2
from fastapi import FastAPI, HTTPException, status
from typing import Optional
from pydantic import BaseModel, HttpUrl
from psycopg2.extras import RealDictCursor

# --- App Initialization ---
app = FastAPI(title="AIQuest Course API")

# --- Database Configuration & Initialization ---
def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    while True:
        try:
            conn = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="123456",
                database="aiquest",
                port="8080"  # Specific port requested by the user
            )
            print('Database connection is open')
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            time.sleep(5)

# Initialize global connection and cursor
conn = get_db_connection()
cursor = conn.cursor(cursor_factory=RealDictCursor)

def init_db():
    """Ensures the necessary database tables exist."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        instructor TEXT NOT NULL,
        duration FLOAT NOT NULL,
        website TEXT NOT NULL
    );
    """)
    conn.commit()

init_db()

# --- Pydantic Schemas ---
class Course(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[float] = None
    website: Optional[HttpUrl] = None

# --- Basic Routes ---
@app.get("/")
def home():
    return {"message": "Welcome to AIQuest FastAPI"}

@app.get("/about")
def about():
    return {"about": "This is a test API for managing courses"}

# --- Course CRUD Routes ---

@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: Course):
    """Creates a new course entry in the database."""
    insert_query = """
        INSERT INTO course (name, instructor, duration, website)
        VALUES (%s, %s, %s, %s)
        RETURNING id, name, instructor, duration, website;
    """
    cursor.execute(insert_query, (course.name, course.instructor, course.duration, str(course.website)))
    new_course = cursor.fetchone()
    conn.commit()
    return {
        "message": f"Course '{course.name}' has been created successfully",
        "course": new_course
    }

@app.get("/courses")
def get_all_courses():
    """Retrieves all courses from the database."""
    cursor.execute("SELECT id, name, instructor, duration, website FROM course ORDER BY id ASC")
    courses = cursor.fetchall()
    return {
        "message": "Courses retrieved successfully",
        "courses": courses
    }

@app.patch("/courses/{id}")
def update_course(id: int, course: CourseUpdate):
    """Updates specific fields of an existing course entry."""
    # Convert the pydantic model to a dict, excluding fields that weren't sent
    update_data = course.dict(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="At least one field must be provided for update")

    # Build the SQL UPDATE statement dynamically
    fields = []
    values = []
    for key, value in update_data.items():
        fields.append(f"{key} = %s")
        # Ensure HttpUrl is converted to a string for the database
        values.append(str(value) if key == "website" else value)
    
    # Add the ID to the end of the values list for the WHERE clause
    values.append(id)
    
    update_query = f"""
        UPDATE course 
        SET {', '.join(fields)}
        WHERE id = %s
        RETURNING id, name, instructor, duration, website;
    """
    
    cursor.execute(update_query, tuple(values))
    updated_course = cursor.fetchone()
    conn.commit()
    
    if not updated_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
    return {
        "message": "Course updated successfully",
        "course": updated_course
    }

@app.get("/courses/{id}")
def get_course_by_id(id: int):
    """Retrieves a single course by its unique ID."""
    cursor.execute("SELECT id, name, instructor, duration, website FROM course WHERE id = %s", (id,))
    course = cursor.fetchone()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {
        "message": "Course retrieved successfully",
        "course": course
    }

@app.delete("/courses/{id}")
def delete_course_by_id(id: int):    
    """Deletes a course from the database and returns its details."""
    delete_query = "DELETE FROM course WHERE id = %s RETURNING id, name, instructor, duration, website"
    cursor.execute(delete_query, (id,))
    deleted_course = cursor.fetchone()
    conn.commit()
    
    if not deleted_course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    return {
        "message": "Course deleted successfully",
        "course": deleted_course
    }