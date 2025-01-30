# learn_fastapi

This repository is dedicated to learning and practicing FastAPI, a powerful web framework for Python. Thanks to this <a href="https://www.youtube.com/watch?v=tLKKmouUams">YouTube video</a>, I was introduced to FastAPI and am already feeling empowered while building APIs!

This repo definitely doesn't cover all features of fastapi but contains **go to fundamentals** for getting started with fastapi. Following steps outline the key concepts and features can be considered as the learning path at beginner level, referring `learn_fastapi.ipynb` and `myapi.py`:

## Learning Steps

1. **fastapi Documentation**

   The <a href="https://fastapi.tiangolo.com/learn/">official fastapi documentation</a> is the best. Solely following it step by step would be enough for anyone. Really, just try it.

   1.1. **Concurrency + Parallelism ==> Web + Machine Learning **

   Read and summarized from <a href="https://fastapi.tiangolo.com/async/">fastapi async</a>:
   
   - `concurrency`: The ability to manage multiple tasks at the same time by quickly switching between them. In FastAPI, this is achieved using asynchronous programming (`async/await`), enabling efficient handling of I/O-bound operations like database queries or API calls without blocking the main thread.
   - `parallelism`: Running multiple tasks simultaneously on different CPU cores. In Python, libraries like multiprocessing or frameworks like FastAPI with workers (e.g., using `gunicorn` with multiple workers) enable parallel execution, which is particularly useful for `CPU-bound` tasks.
      `multiprocessing`: A technique to create separate processes (not threads) to run tasks in parallel, utilizing multiple CPU cores. This is effective for `CPU-bound` tasks in Python, bypassing the Global Interpreter Lock (`GIL`). For FastAPI, multiprocessing can help with heavy computation tasks by delegating them to worker processes.
   - `CPU bound`: A type of task that is limited by the speed of the CPU, such as mathematical computations or data processing. In FastAPI, CPU-bound tasks are better handled using multiprocessing or external workers (e.g., `celery` or `background tasks`) to prevent slowing down the main application thread.

3. **Installation**:

   Need to install `fastapi` library and also need `uvicorn` to run local server. For data validation, `pydantic` is superb which comes preinstalled with fastapi.

   - `pip install fastapi uvicorn`

4. **Folder Structure**

   (not dived much into it yet)

   Depending on the project, it might be a good idea to have separate files for routing, database connection, models and schemas. Its been thoroughly implemented in the <a href="https://github.com/Ahnaf19/hotel_transylvania">**Hotel Transylvania**</a> repo!

5. **Basics**:

   - learn how to initiate `fastapi` application
   - api endpoints or routers
   - CRUD with GET, POST, PUT, DELETE
   - Data validation with pydantic
   - parameters
     - path parameters
     - query parameters
   - request body
   - response model

6. **Run Uvicorn Server**:

   - command to run the app through uvicorn: `uvicorn myapi:app --reload`
     - `myapi` is the name of the py file
     - `app` is the name of the instance of FASTAPI class
     - `reload` flag enables auto reload when changed and saved

7. **Auto Generated API Docs**:

   - learn the most awesome thing of fastapi, the auto generated api documentation
     - swagger UI
     - docly

8. **CRUD**:

   - dive into the depth of CRUD with GET, POST, PUT, DELETE
   - How to validate data with pydantic models

9. **Useful Libraries/approaches/validations**:

   - `fastapi`
     - HTTPException (raising HTTP exception/error)
   - `pydantic`
     - `basemodel`
     - `EmailStr`
     - `validator` (decorator for custom validation)
     - json serialization [`.json()` to json, `.model_dump()` to dict, `.parse_raw()` to pydantic]
   - `uuid`
     - UUID and uuid4 (generate unique id)

10. **Test fastapi**

   - add `__init__.py` in the repo root --> addresses import issues
   - create `tests/` folder to contain all test files
   - add `__init__.py` in the `tests/` folder as well --> pytest can easily detect test files
   - pytest using `fastapi.TestClient`
     - follow `test_myapi.py`

# Let's get ADVANCED!

   If hungry for more: to get habituted with industry standard and good practices of `fastapi`+`pydantic`+`loguru`+`pytest` on how to build+structure+organize from scratch dive into this repo: <a href="https://github.com/Ahnaf19/hotel_transylvania">**Hotel Transylvania**</a>! Its a hotel management system that can handle guest and room CRUD operations. 

   > its an on going project at the moment, so expect some services to be finished soon. [30 Jan, 2025]
   
   This repo includes:

   - API for guests and rooms which is kinda fast --> `fastAPI`
   - Clean & modular repo structure
      - separate application and tests directory
      - clean module/package initiation at each submodule
      - modular structure for required data, schemas, services and routers
   - Clean application
      - Added multiple modular routers to the main
      - can be switched to any other framework easily
   - Use of custom Exception
   - Logging using `loguru`: what a library!
   - `pytest` for unit testing
   - Of course, `github actions` to automate testing (CI)

# Let’s Connect

If you're passionate about testing or Python development, let’s discuss ideas and experiences. Feedback, forks, and collaboration requests are always welcome!
