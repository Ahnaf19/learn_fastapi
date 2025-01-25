from fastapi.testclient import TestClient
from learn_fastapi.myapi import app

# FILE: learn_fastapi/test_myapi.py

client = TestClient(app)

def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
    "1": {
    # 1: {
        "name": "John",
        "age": 17,
        "class_name": "year 12"
    }
    }
    
def test_get_student():
    response = client.get('/get-student/1')
    assert response.status_code == 200
    assert response.json() == {
        "name": "John",
        "age": 17,
        "class_name": "year 12"
    }
    
def test_test_query_param():
    response = client.get('/test-query')
    limit, test = 20, 30
    response2 = client.get(f'/test-query?limit={limit}&test={test}')
    assert response.status_code == 200
    assert response2.status_code == 200
    assert response2.json() == {"data": f"test query param {limit} and test {test}"}

def test_get_student_by_name():
    # sending query using url
    response = client.get('/get-by-name?name=ahnaf&test=1')
    # query can be sent using params too
    response2 = client.get('/get-by-name', params={"name": "John", "test": 1})
    assert response.status_code == 200
    assert response.json() == {"Data": "Not Found"}
    assert response2.status_code == 200
    assert response2.json() == {
        "name": "John",
        "age": 17,
        "class_name": "year 12"
    }
    
def test_create_student():
    # pass path paramerter in the url and the request body in json param
    
    # check response for posting existing student
    response = client.post('/create-student/1',                     
    json={
        "name": "Ahnaf",
        "age": 17,
        "class_name": "year 12"
    })
    assert response.status_code == 200
    assert response.json() == {
        "Error": "Student exists"
    }
    
    # post new student
    response2 = client.post('/create-student/2',                     
    json={
        "name": "Ahnaf",
        "age": 17,
        "class_name": "year 12"
    })
    assert response2.status_code == 200
    assert response2.json() == {
        "name": "Ahnaf",
        "age": 17,
        "class_name": "year 12"
    }
    
    # check if the student is created in the local db
    response3 = client.get('/get-student/2')
    assert response3.status_code == 200
    assert response3.json() == {
        "name": "Ahnaf",
        "age": 17,
        "class_name": "year 12"
    }

def test_update_student():
    # update existing student
    response = client.put('/update-student/1',                     
    json={
        "name": "John Updated",
        "age": 18
    })
    assert response.status_code == 200
    assert response.json() == {
        "name": "John Updated",
        "age": 18,
        "class_name": "year 12"
    }
    
    # update non-existing student
    response2 = client.put('/update-student/3',                     
    json={
        "name": "Non Existing",
        "age": 20
    })
    assert response2.status_code == 200
    assert response2.json() == {
        "Error": "Student does not exist"
    }

def test_delete_student():
    # delete existing student
    response = client.delete('/delete-student/1')
    assert response.status_code == 200
    assert response.json() == {
        "Message": "Student with id 1 deleted successfully"
    }
    
    # delete non-existing student
    response2 = client.delete('/delete-student/3')
    assert response2.status_code == 200
    assert response2.json() == {
        "Error": "Student does not exist"
    }
    
    # verify deletion
    response3 = client.get('/get-student/1')
    assert response3.status_code == 200
    assert response3.json() == {
        "Error": "Student does not exist"
    }