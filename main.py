import time
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# define request body schema
class Course(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456",
            database="aiquest",
            port="8080"  # Standard Postgres port
        )
        print('Database connection is open')
        break
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        time.sleep(5)

cursor = conn.cursor(cursor_factory=RealDictCursor)
# Ensure the courses table exists
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
@app.post("/courses")
def create_course(course: Course):
    insert_query = """
        INSERT INTO course (name, instructor, duration, website)
        VALUES (%s, %s, %s, %s)
        RETURNING id, name, instructor, duration, website;
    """
    cursor.execute(insert_query, (course.name, course.instructor, course.duration, str(course.website)))
    new_course = cursor.fetchone()
    conn.commit()
    return {"message": f"course {course.name} has been created successfully", "course": new_course}


@app.get("/courses")
def get_courses():
    # Explicitly list columns to guarantee the order in the JSON response
    cursor.execute("SELECT id, name, instructor, duration, website FROM course ORDER BY id ASC")
    courses = cursor.fetchall()
    return {"message": "courses retrieved successfully", "courses": courses}



@app.get("/courses/{id}")
def get_courses(id: int):
    cursor.execute("SELECT id, name, instructor, duration, website FROM course WHERE id = %s", (id,))
    course = cursor.fetchone()
    if course:
        return {"message": "course retrieved successfully", "course": course}
    else:
        return {"message": "course not found"}


@app.delete("/courses/{id}")
def delete_courses(id: int):    
    cursor.execute("DELETE FROM course WHERE id = %s RETURNING id, name, instructor, duration, website", (id,))
    deleted_course = cursor.fetchone()
    conn.commit()
    if deleted_course:  
        return {"message": "course deleted successfully", "course": deleted_course}
    else:
        return {"message": "course not found"}
        
@app.get("/")
def aiquest():
    return {'fast':'api'}

@app.get("/about")
def about():
    return {'about':'test api'}