from marshmallow import Schema, fields


class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    # description = fields.Str()


incomming_book_data = {
    "title": "Clean Code",
    "author": "Bob Martin",
    # "description": "A book about writting cleaner code.",
}

class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author

book_schema = BookSchema()
book = book_schema.load(incomming_book_data)
book_obj = Book(**book)

print(book_obj.title)
print(book_obj.author)
