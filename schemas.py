from pydantic import BaseModel

class BookBase(BaseModel):
    name: str
    description: str
    pages: int
    author: str
    publisher: str

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True
