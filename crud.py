from fastapi import FastAPI , Body

app =  FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Two', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get('/books/mybook')
async def read_all_books():
    return BOOKS

@app.get('/test/{dynamic}')  #always have apis with dynamic queries after normal apis
async def read_all_books(dynamic : str):
        return {"dynamic":dynamic}


@app.get('/books/')
async def read_category_by_query(category : str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold() :
            books_to_return.append(book)
    return books_to_return

@app.get('/books/{book_title}')  #always have apis with dynamic queries after normal apis
async def read_all_books_by_title(book_title : str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get('/books/{book_author}/')  #always have apis with dynamic queries after normal apis
async def read_by_author(book_author : str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return



@app.post('/create_book')
async def create_book(new_book = Body()):
    BOOKS.append(new_book)



@app.put('/update_book')
async def update_book(updated_book = Body()):
    for book in BOOKS:
        if book.get('title').casefold() == updated_book.get('title').casefold():
            book.update(updated_book)


@app.delete('/delete_book_by_title/')
async def delete_book(delete_book_by_title):
    for book in BOOKS.copy():
        if delete_book_by_title.casefold() == book.get('title').casefold():
            BOOKS.remove(book)

@app.delete('/delete_book_by_author/')
async def delete_book(delete_book_by_author):
    for book in BOOKS:
        if delete_book_by_author.casefold() == book.get('author').casefold():
            BOOKS.remove(book)
            break


@app.patch('/update_partial')
async def update_partial(updated_partial = Body()):
    for book in BOOKS:
        if updated_partial.get('title').casefold() == book.get('title').casefold():
            for key , val in updated_partial.items():
                if key in book and val is not None:
                    book[key]=val
            return {"message":"updated"}
    return {"message":"error"}

@app.get('/books_from_author')
async def books_from_author(author : str | None = None):
        return [book for book in BOOKS if book.get('author').casefold()==author.casefold()] 
    
@app.get('/books/books_from_author/{author}')
async def books_from_author(author : str | None = None):
    
        return [book for book in BOOKS if book.get('author').casefold()==author.casefold()] 
    
