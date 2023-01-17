from fastapi import FastAPI

from routers.users import router as UserRouter
from routers.posts import router as PostRouter

app = FastAPI()

app.include_router(UserRouter)
app.include_router(PostRouter)

@app.get("/")
async def root():
    return {"FastApi workout": "Project to explore features of framework."}
