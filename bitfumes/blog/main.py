from fastapi import FastAPI
from . import schemas, models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return {"index": "oh nooo"}

@app.post('/blog')
def create(request: schemas.Blog):
    return request