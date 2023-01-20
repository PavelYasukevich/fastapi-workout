import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI

from routers.posts import router as PostRouter
from routers.users import router as UserRouter

load_dotenv()

DBNAME = os.environ.get("DBNAME")
DB_USER = os.environ.get("DB_USER")

app = FastAPI()
app.include_router(UserRouter)
app.include_router(PostRouter)


@app.get("/")
async def root():
    return {"FastApi workout": "Project to explore features of framework."}


with psycopg.connect(f"dbname={DBNAME} user={DB_USER}") as conn:
    with conn.cursor() as cur:
        print(cur.execute("SELECT * FROM posts").fetchone())
