from app import db
from app.models.book import Book
from flask import Blueprint, request, make_response, jsonify


books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", strict_slashes=False, methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        title_query = request.args.get("title")
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else: 
            books = Book.query.order_by(Book.id).all()
        # books = Book.query.filter(Book.id >= 20).all() # Example of filtering
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"],
                        description=request_body["description"])

        db.session.add(new_book)
        db.session.commit()
        return make_response(f"Book {new_book.title} successfully created with id {new_book.id}", 201)


@books_bp.route("/<book_id>", strict_slashes=False, methods=["GET", "PUT", "PATCH", "DELETE"])
def handle_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return make_response(f"Book {book_id} not found", 404)

    if request.method == "GET":
        return {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }
    elif request.method == "PUT":
        form_data = request.get_json()
        book.title = form_data["title"],
        book.description = form_data["description"]

        db.session.commit()

        return make_response(f"Book {book_id} successfully updated")
    
    elif request.method == "PATCH":
        form_data = request.get_json()
        
        for key, value in form_data.items():
            if key in dir(book):  # nod towards data validation - checking that given key is a valid attribute 
                setattr(book, key, value)
        # Alternative, more explicit method:
        # if "title" in form_data.keys():
        #     book.title = form_data["title"]
        # if "description" in form_data.keys():
        #     book.description = form_data["description"]
        db.session.commit()       
        return make_response(f"Book {book_id} successfully updated")

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book {book_id} successfully deleted")
    
@books_bp.route("/top_three", strict_slashes=False, methods=["GET"])
def handle_top_three_books():
        books = Book.query.order_by(Book.id).limit(3).all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)
    
