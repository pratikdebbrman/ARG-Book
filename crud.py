from sqlalchemy.orm import Session
from models import Book

def create_book(db: Session, name: str, description: str, pages: int, author: str, publisher: str):
    db_book = Book(name=name, description=description, pages=pages, author=author, publisher=publisher)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session, author: str = None, publisher: str = None):
    query = db.query(Book)
    if author:
        query = query.filter(Book.author == author)
    if publisher:
        query = query.filter(Book.publisher == publisher)
    return query.all()

def delete_book(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
