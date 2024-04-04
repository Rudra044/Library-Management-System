from flask import Flask, request, jsonify, Blueprint
from flask_migrate import Migrate
from app.models.models import db, Books
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.utils import new_add, delete, update_details



bp = bp = Blueprint('authe', __name__, url_prefix='/auth')


@bp.route('/book/add', methods=['POST'])
@jwt_required()
def add_book():
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    genre = data.get('genre')
    publication_year = data.get('publication_year') 
    if title and author and isbn and publication_year:
        if Books.query.filter(db.and_(Books.profile_id == user_id, Books.title == title, Books.author == author)).first():
            return jsonify({'error':'Book is already added by you. '}),400
        else:
            new_book = Books(title=title, author=author, isbn=isbn,
                             genre=genre, publication_year=publication_year, 
                             profile_id=user_id)
            new_add(new_book)
            return jsonify({'message': 'New book added'}),201
    else:
        return jsonify({'error':
                    'Provide valid such fields, Title , Author  , ISBN , Publication_year these fields must be provided.'}),400
    
    
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
    book = Books.query.filter(db.and_(Books.profile_id == user_id, Books.id == book_id)).first()
    if not book:
        return jsonify({'error': 'Book is not present.'}),400
    
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
    return jsonify({'message': 'Book details updated successfully'})
    

@bp.route('/book/delete/<int:book_id>', methods=['DELETE'])
@jwt_required()
def delete_book_details(book_id):
    user_id = get_jwt_identity()
    book = Books.query.filter(db.and_(Books.profile_id == user_id, Books.id == book_id)).first()
    if book:
        delete(book)
        return jsonify({'message': 'Book deleted'})
    else:
        return jsonify({'error': 'Book is not added by you.'}),400


@bp.route('/book', defaults={'book_id': None}, methods=['GET'])
@bp.route('/book/<int:book_id>', methods=['GET'])
def get_books(book_id):
    if book_id is None:
        all_books = Books.query.all()
        book_list = []
        for book in all_books:
            book_list.append({
                'id': book.id,
                'title': book.title, })
        return jsonify(book_list)
    book = Books.query.get(book_id)
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
        return jsonify({'error': 'Book not found'}),404