from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session
from models import SessionLocal, Movie, User, Rating

app = FastAPI(title="MovieFlix API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

class MovieIn(BaseModel):
    title: str
    year: int | None = None
    genre: str | None = None
    country: str | None = None

class MovieOut(MovieIn):
    id: int
    class Config:
        from_attributes = True

class UserIn(BaseModel):
    name: str
    age: int | None = None
    country: str | None = None

class UserOut(UserIn):
    id: int
    class Config:
        from_attributes = True

class RatingIn(BaseModel):
    user_id: int
    movie_id: int
    score: float = Field(ge=1, le=5)

class RatingOut(RatingIn):
    id: int
    class Config:
        from_attributes = True

@app.post("/movies", response_model=MovieOut)
def create_movie(payload: MovieIn, db: Session = Depends(get_db)):
    obj = Movie(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/movies", response_model=List[MovieOut])
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@app.post("/users", response_model=UserOut)
def create_user(payload: UserIn, db: Session = Depends(get_db)):
    obj = User(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/ratings", response_model=RatingOut)
def create_rating(payload: RatingIn, db: Session = Depends(get_db)):
    if not db.query(User).filter_by(id=payload.user_id).first():
        raise HTTPException(400, detail="user_id inexistente")
    if not db.query(Movie).filter_by(id=payload.movie_id).first():
        raise HTTPException(400, detail="movie_id inexistente")
    obj = Rating(**payload.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/ratings", response_model=List[RatingOut])
def list_ratings(db: Session = Depends(get_db)):
    return db.query(Rating).all()
