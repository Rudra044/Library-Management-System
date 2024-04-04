from flask import Flask, request, jsonify , Blueprint
from flask_migrate import Migrate
from app.models.models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from urllib.parse import unquote_plus, quote_plus
from config import Config
import os
from app.utils import new_add, delete, update_details
from app import bcrypt,mail


bp = bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route("/register", methods=['POST'])
def create_user():
    data = request.json
    email_id = data.get('email_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')
    password = data.get('password')

    if email_id and password:
        if User.query.filter_by(email_id=email_id).first():
            return jsonify({'error': 'User with this email or username already exists'}),400
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email_id=email_id, first_name=first_name, last_name=last_name,
                        phone_number=phone_number, password=hashed_password)
        new_add(new_user)
        return jsonify({'message': 'User created successfully'}),201
    else:
        return jsonify({'error': 'All fields need to be provided'}),400


@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email_id = data.get('email_id')
    password = data.get('password')
    user = User.query.filter_by(email_id=email_id).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid email or password'}),400

   
@bp.route('/information', methods=['GET'])
@jwt_required()
def get_data_by_id():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({
            'id': user.id,
            'email_id': user.email_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number, })
    

@bp.route('/update', methods=['PATCH'])
@jwt_required()
def update_information():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}),404
    data = request.json
    phone_number = data.get('phone_number')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if not phone_number:
        if not first_name:
            if not last_name:
                return jsonify({'message': 'invalid input'}),400

    if phone_number:
        user.phone_number = phone_number
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    update_details()
    return jsonify({'message': 'User details are updated successfully'}),201


@bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        delete(user)
        return jsonify({'message': 'Your profile is deleted'}),201
    else:
        return jsonify({'error': 'No user profile to be deleted'}),404


@bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.json
    password = data.get('password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}),400
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Incorrect password'}),400
    if not new_password:
        return jsonify({'message': 'New password not provided'}),400
    if not confirm_new_password:
        return jsonify({'message': 'Confirm_New password not provided'}),400
    if confirm_new_password != new_password:
        return jsonify({'message': 'Confirm_New password and new password field not match'}),400
    else:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        update_details()
        return jsonify({'message': 'Password changed successfully'}),201


@bp.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.json
    email_id = data.get('email_id')
    user = User.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'User not found'}),404
    else:  
        encoded_email_id = quote_plus(email_id) 
        reset_link = f'http://127.0.0.1:5000/reset_password/{encoded_email_id}'
        msg = Message( 'Hello', 
                sender=os.getenv('MAIL_USERNAME'),
                recipients=[email_id]) 
        msg.body =  f'Hello,\n\nYour reset link is/ {reset_link}'
        mail.send(msg) 

        return jsonify({'message': 'The Mail is Send.'}),201


@bp.route('/reset_password/<encoded_email_id>', methods=['POST'])
def reset_password(encoded_email_id):

    email_id = unquote_plus(encoded_email_id)  
    data = request.json
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
    user = User.query.filter_by(email_id=email_id).first()
    if not user:
        return jsonify({'message': 'Invalid email ID'}),400
    if not new_password:
        return jsonify({'message': 'New password not provided'}),400
    if not confirm_new_password:
        return jsonify({'message': 'Confirm_New password not provided'}),400
    if confirm_new_password != new_password:
        return jsonify({'message': 'Confirm_New password and new password field not match'}),400
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    update_details()
    return jsonify({'message': 'Password reset successfully'}),201
