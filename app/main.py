from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/", tags=["Health Check"], status_code=status.HTTP_200_OK)
async def health_check():
    return {"message": "API Service is up and running!"}