from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, votes, wishes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="许愿池 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wishes.router)
app.include_router(votes.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "许愿池 API 运行中"}
