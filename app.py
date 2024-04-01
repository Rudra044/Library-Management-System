from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Profile , db , Books , Author
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail,Message
from urllib.parse import unquote_plus, quote_plus
from config import Config
import os


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate=Migrate(app,db)
mail=Mail(app)

@app.route("/register",methods=['POST'])
def create_user():
     data = request.json
     email_id = data.get('email_id')
     first_name = data.get('first_name')
     last_name= data.get('last_name')
     phone_number=data.get('phone_number')
     password = data.get('password')
     if email_id and password:
        if Profile.query.filter_by(email_id=email_id).first():
            return jsonify({'error': 'User with this email or username already exists'})
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Profile(email_id=email_id, first_name=first_name, last_name=last_name,
                       phone_number=phone_number, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
     else:
        return jsonify({'error': 'All fields need to be provided'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email_id=data.get('email_id')
    password=data.get('password')
    user = Profile.query.filter_by(email_id=email_id).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid email or password'})
    
@app.route('/information/<int:user_id>',methods=['GET'])
@jwt_required()
def get_data_by_id(user_id):
     user = Profile.query.filter_by(id=user_id).first()
     return jsonify(user)
    

@app.route('/update',methods=['PATCH'])
@jwt_required()
def update_phone():
    user_id = get_jwt_identity()
    user = Profile.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    data = request.json
    phone_number=data.get('phone_number')
    first_name = data.get('first_name')
    last_name= data.get('last_name')
    if not phone_number and first_name and last_name:
        return jsonify({'message': 'invalid input'})

    if phone_number:
        user.phone_number = phone_number
    if first_name:
        user.first_name = first_name
    if last_name:
       user.last_name = last_name
    db.session.commit() 
    return jsonify({'message': 'User details are updated successfully'})  


@app.route('/delete',methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = Profile.query.filter_by(id=user_id).first()
    if user:
       db.session.delete(user)
       db.session.commit()
       return jsonify({'message': 'data deleted'})
    else:
        return jsonify({'error': 'User cannot be deleted'})


@app.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.json
    password = data.get('password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
    
    user = Profile.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'})

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Incorrect password'})

    if not new_password:
        return jsonify({'message': 'New password not provided'})
    if not confirm_new_password:
        return jsonify({'message': 'Confirm_New password not provided'})
    if confirm_new_password != new_password:
        return jsonify({'message': 'Confirm_New password and new password field not match'})
    else:

        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'})


@app.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.json
    email_id=data.get('email_id')
    user = Profile.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'User not found'})
    else:  
         encoded_email_id = quote_plus(email_id) 
         reset_link = f'http://127.0.0.1:5000/reset_password/{encoded_email_id}'
         msg = Message( 
                'Hello', 
                sender = os.getenv('MAIL_USERNAME'),
                recipients = [email_id]) 
         msg.body =  f'Hello,\n\nYour reset link is/ {reset_link}'
         mail.send(msg) 

         return jsonify({'message': 'The Mail is Send.'}) 


@app.route('/reset_password/<encoded_email_id>', methods=['POST'])
def reset_password(encoded_email_id):

    email_id = unquote_plus(encoded_email_id)  
    data = request.json
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
   
    user = Profile.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'Invalid email ID'})
    if confirm_new_password != new_password:
        return jsonify({'message': 'Confirm_New password and new password field not match'})

    
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    db.session.commit()
    
    return jsonify({'message': 'Password reset successfully'})



"""
##########here the code starts for book.py############## 

"""

@app.route('/book/add', methods=['POST'])
@jwt_required()
def add_book():
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    author = data.get('author')
    isbn= data.get('isbn')
    genre = data.get('genre')
    publication_year = data.get('publication_year') 
    if title and author and isbn and publication_year:
         if Books.query.filter(db.and_(Books.profile_id==user_id , Books.title==title)).first():
             return jsonify({'error':'Book is already added by you. '})
         else:
             
            new_book = Books(title = title, author = author,isbn = isbn,genre = genre,publication_year= publication_year
                         ,profile_id=user_id)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({'message': 'New book added'})
    else:
        return jsonify({'error': 'Provide valid such fields, Title , Author  , ISBN , Publication_year these fields must be provided.'})
    
    
@app.route('/book/update', methods=['PATCH'])
@jwt_required()
def update_book_details():
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    author = data.get('author')
    isbn = data.get('isbn')
    genre = data.get('genre')
    publication_year = data.get('publication_year')

    book= Books.query.filter(db.and_(  Books.profile_id==user_id , Books.title==title )).first()
    if not book:
       return jsonify({'error':'Book is not present.'})
       
    if author:
        book.Author = author
    if isbn:
        book.ISBN = isbn
    if publication_year:
        book.Publication_year = publication_year
    if genre:
        book.genre = genre
    db.session.commit() 
    return jsonify({'message': 'Book details updated successfully'})
    

@app.route('/book/delete', methods=['DELETE'])
@jwt_required()
def delete_book_details():
    user_id = get_jwt_identity()
    data = request.json
    title = data.get('title')
    book= Books.query.filter(db.and_(Books.profile_id==user_id , Books.title==title)).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted'})
    else:
        return jsonify({'error':'Book is not added by you.'})


@app.route('/books', methods=['GET'])
def get_books():
    all_books = Books.query.all()
    book_list = []
    for book in all_books:
        book_list.append({
            'id': book.id,
            'title': book.title,
        })
    return jsonify(book_list)

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
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
        return jsonify({'error': 'Book not found'})
    


    """



    Author Mangemnt
    
    
    """


@app.route('/author/add', methods=['POST'])
@jwt_required()
def add_author():
    user_id = get_jwt_identity()
    data = request.json
    author_name = data.get('author_name')
    biography = data.get('biography')
    nationality = data.get('nationality') 
    if  author_name:
         if Author.query.filter(db.and_(profile_id=user_id , author_name=author_name)).first():
             return jsonify({'error':'Author is already added by you.'})
         else:
             
            new_author = Author(author_name = author_name, biography = biography,nationality = nationality
                         ,profile_id=user_id)
            db.session.add(new_author)
            db.session.commit()
            return jsonify({'message': 'New book added'})
    else:
        return jsonify({'error': 'Provide valid fields' })
    









if __name__ == "__main__":
    app.run(debug=True)