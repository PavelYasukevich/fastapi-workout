from fastapi import FastAPI

from routers.users import router as UserRouter

app = FastAPI()

app.include_router(UserRouter)


@app.get("/")
async def root():
    return {"Hello": "World"}
