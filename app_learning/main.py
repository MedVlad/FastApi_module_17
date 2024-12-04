from itertools import product

from fastapi import FastAPI
from routers  import category


app = FastAPI()

@app.get("/")
async def welcome():
    return {"message":"My shop"}

app.include_router(category.router)
app.include_router(products.router)