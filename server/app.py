#!/usr/bin/env python3
import os
from flask import request
from flask_restful import Resource
from config import create_app, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        schema = BookSchema()
        return schema.dump(book), 200

class Books(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        paginated = Book.query.paginate(page=page, per_page=per_page, error_out=False)
        schema = BookSchema(many=True)
        items = schema.dump(paginated.items)

        response = {
            "page": paginated.page,
            "per_page": paginated.per_page,
            "total": paginated.total,
            "total_pages": paginated.pages,
            "items": items
        }
        return response, 200

# REGISTER resources HERE
api.add_resource(BookResource, '/book/<int:book_id>', endpoint='book')
api.add_resource(Books, '/books', endpoint='books')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
