from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, Base
from models import Book
import crud
import auth
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(auth.verify_token)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return token

@app.post("/token")
def login(username: str, password: str):
    # Simplified authentication logic
    if username == "admin" and password == "password":
        access_token = auth.create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/books/", response_model=schemas.BookResponse)
def create_book(
     name: str = Query(...),
    description: str = Query(...),
    pages: int = Query(...),
    author: str = Query(...),
    publisher: str = Query(...),
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user)
):
    db_book = crud.create_book(
        db=db,
        name=name,
        description=description,
        pages=pages,
        author=author,
        publisher=publisher
    )
    return db_book

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(
    book_id: int,
    author: str = Query(None),
    publisher: str = Query(None),
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user)
):
    if author or publisher:
        books = crud.get_books(db=db, author=author, publisher=publisher)
        book = next((book for book in books if book.id == book_id), None)
    else:
        book = crud.get_book(db=db, book_id=book_id)

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}", response_model=schemas.BookResponse)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user)
):
    db_book = crud.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
