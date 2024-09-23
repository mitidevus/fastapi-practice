from fastapi import FastAPI

from routers import post

app = FastAPI()

app.include_router(post.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"