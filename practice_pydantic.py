
from pydantic import BaseModel
from fastapi import HTTPException, FastAPI, Request
import logging
import time


logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

app = FastAPI(title="Students")

students = [
    {"id": 1, "name": "Dana", "age": 24, "city": "Haifa"},
    {"id": 2, "name": "Avi", "age": 31, "city": "Tel Aviv"},
    {"id": 3, "name": "Noa", "age": 22, "city": "Haifa"},
]

@app.middleware("http")
async def log_requests(request: Request, call_text):
    start = time.time()
    response = await call_text(request)
    ms = round((time.time() - start) * 1000, 1)
    logging.info(request.method + " " + request.url.path + " -> "
                 + str(response.status_code) + " (" + str(ms) + " ms)")
    response.headers["X-proceed-time"] = str(ms)
    return response

class StudentIn(BaseModel):
    name: str
    age: int
    city: str = "Unknown"


@app.get("/students")
def print_students(city: str | None = None, min_age: int = 0, limit: int = 10):
    result = []
    for student in students:
        if city is not None and student["city"] != city:
            continue
        if student["age"] < min_age:
            continue
        result.append(student)
    return result[:limit]

@app.get("/students/{student_id}")
def get_specific_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Oops, couldn't found id")

@app.post("/students")
def add_student(student: StudentIn):
    new_id = students[-1]["id"] + 1
    new_student = {"id": new_id, "name": student.name, "age": student.age, "city": student.city}
    students.append(new_student)
    return new_student

@app.delete("/students/{name}")
def delete_student(name: str):
    for i in range(len(students)):
        if students[i]["name"] == name:
            students.pop(i)
            return students
    raise HTTPException(status_code=404, detail="Couldn't find student")

@app.put("/students/{id}")
def update_students_age(id: int, req: StudentIn):
    for student in students:
        if student["id"] == id:
            student["name"] = req.name
            student["age"] = req.age
            student["city"] = req.city
            return student
    raise HTTPException(status_code=404, detail="Couldn't find id")
