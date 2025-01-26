# freecodecamp youtube link
# https://www.youtube.com/watch?v=tLKKmouUams

from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

# app initiation
app = FastAPI()

# local database for testing
# add comment 1
# add commment 2
# add comment 3
students: dict[int, dict[str, str|int]] = {
    1: {
        "name": "John",
        "age": 17,
        "class_name": "year 12"
    }
}

# pydantic schemas
class Student(BaseModel):
    name: str
    age: int
    class_name: str
    
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    class_name: Optional[str] = None   

# endpoints or routes
@app.get('/')
def index():
    # return {"name": "First Data"}
    return students

@app.get('/get-student/{student_id}')
def get_student(student_id: int = Path(description="The ID of the student you want to view", gt=0, lt=3)):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    return students[student_id]
# * commonly: 
# gt = greater than
# lt = less than
# ge = greater than or equal to
# le = less than or equal to
# multiple validation can be done by using tuple
# example: gt=0, lt=3, le=2, ge=1
# if we want to make the parameter optional, we can use None
# example: student_id: int = None
# if we want to make the parameter required, we can use ...
# example: student_id: int = Path(...)
# if we want to make the parameter required with a default value, we can use ...
# example: student_id: int = Path(..., default=1)

@app.get('/test-query')
def test_query_param(limit: int = 10, test: int = 0):
    return {"data": f"test query param {limit} and test {test}"}

@app.get('/get-by-name')
def get_student_by_name(*, name: Optional[str] = Query(None, description="The name of the student you want to view"), test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}

@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student.model_dump() # Convert Student object to dictionary using model_dump
    return students[student_id]

@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    # students[student_id] = student.model_dump()
    # if student.name != None:
    #     students[student_id]["name"] = student.name
    # if student.age != None:
    #     students[student_id]["age"] = student.age
    # if student.class_name != None:
    #     students[student_id]["class_name"] = student.class_name
    update_data = student.model_dump(exclude_unset=True) # exclude_unset will exclude the data that is not set/updated
    students[student_id].update(update_data) # update the data
        
    return students[student_id]

@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": f"Student with id {student_id} deleted successfully"}