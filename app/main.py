from fastapi import FastAPI

from routers import post, user

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

@app.get("/", tags=["Health Check"])
async def health_check():
    return "API Service is up and running!"