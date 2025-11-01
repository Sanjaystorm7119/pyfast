from fastapi import FastAPI , HTTPException, Body
from pydantic import BaseModel, Field 
from typing import Optional
from datetime import date
app = FastAPI()


class Book:
    id : int 
    title : str
    author : str
    genre : str
    rating : int
    published_date : date

    def __init__(self, id, title , author, genre , rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.rating = rating
        self.published_date = published_date

class Book_request(BaseModel):
    id : Optional[int] = Field(description="ID not needed",default=None)
    title : str = Field(min_length=3)
    author : str = Field(min_length=2)
    genre : str = Field(min_length=1 , max_length=20)
    rating : int = Field(gt=0,le=5)
    published_date : date = Field()

    model_config = {
        "json_schema_extra" : {
            "example" :{
            "title":"new book",
            "author" : "no-one",
            "genre" : "new genre",
            "rating" : 5,
            "published_date" : "2025-10-30"
            }
        }
    }

BOOKS = [
    Book(1, "abc", "jay", "fun", 3, date(2025, 10, 30)),
    Book(2, "abcd", "san", "fun", 4, date(2025, 10, 29)),
    Book(3, "abcde", "sri", "fun", 5, date(2025, 10, 28)),
    Book(4, "abc", "jay", "fun", 3, date(2025, 10, 25)),
    Book(5, "abc", "jay", "fun", 3, date(2025, 10, 24)),
]

@app.get('/book')
async def get_all_books():
    return BOOKS

@app.get('/idBookFetch')
async def idB_book_fetch(id : int):
    for book in BOOKS:
        if book.id == id :
            return book.__dict__

@app.post('/create_book')
async def create_book(book_req : Book_request):
    new_book = Book(**book_req.model_dump())
    BOOKS.append(find_book_id(new_book))
    return {"message": "Book created", "book": new_book.__dict__}

def find_book_id(book:Book):
    # if len(BOOKS) > 0 :
    #     book.id = BOOKS[-1].id+1
    # else :
    #     book.id = 1
    book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id + 1
    return book


@app.get('/book/')
async def get_book_by_rating(rating: int):
    return [book for book in BOOKS if book.rating == rating]

# @app.put('/books/update')
# async def update_book(id : int , updated_book :dict = Body(...)):
#     for i in range(len(BOOKS)):
#         if BOOKS[i].id == id :
#             # for key , val in updated_book.items():
#             #     if hasattr(book,key):
#             #         setattr(book,key,val)
#             BOOKS[i] = updated_book
#             return {"message":"Updated"}
#     raise HTTPException(status_code=404, detail="not found")

@app.put('/books/update')
async def update_book(book: Book_request):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id :
            # for key , val in updated_book.items():
            #     if hasattr(book,key):
            #         setattr(book,key,val)
            BOOKS[i] = book
            return {"message":"Updated"}
    raise HTTPException(status_code=404, detail="not found")


@app.patch('/books/update_partial')
async def update_partial(id : int , updated_values : dict = Body(...,description="partial update")):
    for book in BOOKS:
        if book.id == id :
            for key,val in updated_values.items():
                if hasattr(book,key):
                    setattr(book,key,val)
            return {"message":"partially updated"}
    raise HTTPException(status_code=404 , detail="not found")

@app.delete('/delete_all_id')
async def delete_book_all(id : int):
    # for i,book in enumerate(BOOKS):
    #     if book.id == id:
    #         BOOKS.pop(i)
    BOOKS[:] = [book for book in BOOKS if book.id != id]
    return {"message":"deleted"}

@app.delete('/delete_one')
async def delete_book_one(id : int):
    for i,book in enumerate(BOOKS):
        if book.id == id:
            BOOKS.pop(i)
            break
    return {"message":"deleted"}


@app.delete('/delete_by_author')
async def delete_by_author(author : str):
    BOOKS[:] = [book for book in BOOKS if book.author.casefold() != author.casefold()]
