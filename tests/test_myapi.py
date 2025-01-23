import pytest
from fastapi.testclient import TestClient
from learn_fastapi.myapi import app

# FILE: learn_fastapi/test_myapi.py


client = TestClient(app)

def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
    "1": {
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
    response = client.post('/create-student/2',                     
    json={
        "name": "Ahnaf",
        "age": 17,
        "class_name": "year 12"
    })
    assert response.status_code == 200
    assert response.json() == {
        "name": "Ahnaf",
        "age": 17,
        "class_name": "year 12"
    }