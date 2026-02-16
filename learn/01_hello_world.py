# ============================================================
# STEP 1: Hello World — Your First FastAPI App
# ============================================================
# Run: uvicorn learn.01_hello_world:app --reload
# Docs: http://127.0.0.1:8000/docs   (Swagger UI)
#       http://127.0.0.1:8000/redoc  (ReDoc)
# ============================================================

from fastapi import FastAPI

# Create the FastAPI application instance.
# title, description, version all show up in /docs automatically.
app = FastAPI(
    title="Hello World API",
    description="The simplest possible FastAPI app — a great starting point.",
    version="1.0.0",
)


# A "route" or "endpoint" is defined with a decorator.
# @app.get("/") means: when a GET request hits "/", run this function.
@app.get("/")
async def root():
    # Return any Python dict — FastAPI serializes it to JSON automatically.
    return {"message": "Hello, World!"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Hello World API"}


# ============================================================
# KEY TAKEAWAYS:
#   1. FastAPI() creates the app — give it a title & description.
#   2. @app.get("/path") registers an endpoint.
#   3. Return a dict → FastAPI turns it into JSON.
#   4. Visit /docs for auto-generated interactive documentation.
#   5. async def is recommended (FastAPI is async-first).
# ============================================================
