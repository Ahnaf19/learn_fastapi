# learn_fastapi

This repository is dedicated to learning and practicing FastAPI, a powerful web framework for Python. Thanks to this <a href="https://www.youtube.com/watch?v=tLKKmouUams">YouTube video</a>, I was introduced to FastAPI and am already feeling empowered while building APIs!

This repo definitely doesn't cover all features of fastapi but contains **go to fundamentals** for getting started with fastapi. Following steps outline the key concepts and features can be considered as the learning path at beginner level, referring `learn_fastapi.ipynb` and `myapi.py`:

## Learning Steps

1. **fastapi Documentation**

   The <a href="https://fastapi.tiangolo.com/learn/">official fastapi documentation</a> is the best. Solely following it step by step would be enough for anyone. Really, just try it.

2. **Installation**:

   Need to install `fastapi` library and also need `uvicorn` to run local server. For data validation, `pydantic` is superb which comes preinstalled with fastapi.

   - `pip install fastapi uvicorn`

3. **Folder Structure**

   (not dived much into it yet)

   Depending on the project, it might be a good idea to have separate files for routing, database connection, models and schemas.

4. **Basics**:

   - learn how to initiate fastapi application
   - api endpoints or routers
   - CRUD with GET, POST, PUT, DELETE
   - parameters
     - path parameters
     - query parameters
   - request body
   - response model

5. **Run Uvicorn Server**:

   - command to run the app through uvicorn: `uvicorn myapi:app --reload`
     - `myapi` is the name of the py file
     - `app` is the name of the instance of FASTAPI class
     - `reload` flag enables auto reload when changed and saved

6. **Auto Generated API Docs**:

   - learn the most awesome thing of fastapi, the auto generated api documentation
     - swagger UI
     - docly

7. **CRUD**:

   - dive into the depth of CRUD with GET, POST, PUT, DELETE
   - How to validate data with pydantic models

8. ## **Useful Libraries/approaches/validations**:

   - fastapi
     - HTTPException (raising HTTP exception/error)
   - pydantic
     - `basemodel`
     - `EmailStr`
     - `validator` (decorator for custom validation)
     - json serialization [`.json()` to json, `.model_dump()` to dict, `.parse_raw()` to pydantic]
   - uuid
     - UUID and uuid4 (generate unique id)

# Yet to be added

- Multifile app route code
- Exception handle (custom class)
  - create a 8 digit pass constraints, if invoked throw exception
  - user exists then custom exception throw
  - request header read (depends, dependency)
- fastapi authentication
- use of cookiecutter (check for fastapi)
- test for fastapi
- custom decorator and concept: collect response time

# Let’s Connect

If you're passionate about testing or Python development, let’s discuss ideas and experiences. Feedback, forks, and collaboration requests are always welcome!
