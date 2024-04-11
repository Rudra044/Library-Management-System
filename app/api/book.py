from flask import Flask, request, jsonify, Blueprint
from app.models.models import db, Books
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import new_add, delete, update_details
from app.services.library_services import book_filter, book_id_filter, book_get, book_all
from app.error_management.success import success_response
from app.error_management.error import error_response
from app.validators.validation import check_book_required_fields



bp = bp = Blueprint('authe', __name__, url_prefix='/auth')


@bp.route('/book/add', methods=['POST'])
@jwt_required()
def add_book():
    user_id = get_jwt_identity()
    data = request.json
    if not check_book_required_fields(data):
        return error_response("0400",  'Mandatory fields need to be provided')
    if  book_filter(user_id,data.get('title'),data.get('author')):
        return error_response("0400", 'Book is already added by you.')
    else:
        new_book = Books(data.get('title'),data.get('author'),data.get('isbn'),
                             data.get('genre'), data.get('publication_year'), 
                             profile_id=user_id)
        new_add(new_book)
        book_data = {
        'email_id': new_book.email_id,
        'first_name': new_book.first_name,
        'last_name': new_book.last_name,
        'phone_number': new_book.phone_number
    }
        return success_response(201, "Success", "New book added",book_data)
    
    
@bp.route('/book/update/<int:book_id>', methods=['PATCH'])
@jwt_required()
def update_book_details(book_id):
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    genre = data.get('genre')
    publication_year = data.get('publication_year')
    book = book_id_filter(user_id,book_id)
    if not book:
        return error_response("0404",  'Book not found')  
    
    if title:
        book.title = title
    if author:
        book.Author = author
    if isbn:
        book.ISBN = isbn
    if publication_year:
        book.Publication_year = publication_year
    if genre:
        book.genre = genre
    update_details()
    book_data = {
        'email_id': book.email_id,
        'first_name': book.first_name,
        'last_name': book.last_name,
        'phone_number': book.phone_number
    }
    return success_response(200, "Success", "Book details updated successfully",book_data)
    

@bp.route('/book/delete/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book_details(book_id):
    user_id = get_jwt_identity()
    book = book_id_filter(user_id,book_id)
    if book:
        delete(book)
        return success_response(200, "Success",  "Book deleted")

    else:
        return error_response("0400", 'Book is not added by you')


@bp.route('/book', defaults={'book_id': None}, methods=['GET'])
@bp.route('/book/<int:book_id>', methods=['GET'])
def get_books(book_id):
    if book_id is None:
        all_books = book_all()
        book_list = []
        for book in all_books:
            book_list.append({
                'id': book.id,
                'title': book.title, })
        return jsonify(book_list)
    book = book_get(book_id)
    if book:
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'genre': book.genre,
            'publication_year': book.publication_year
        })
    else:
       return error_response("0404", 'Book not found') 