from flask import Flask, request, jsonify , Blueprint
from app.models.models import User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
import base64, secrets
import os
from datetime import datetime, timedelta
from app.utils import new_add, delete, update_details
from app import bcrypt,mail
from app.services.customer_services import user_filter, user_filter_id, user_filter_token
from app.error_management.success import success_response
from app.error_management.error import error_response
from app.validators.validation import check_user_required_fields

expires = datetime.now() + timedelta(seconds=30)
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/register", methods=['POST'])
def create_user():
    data = request.json
    if not check_user_required_fields(data):
        return error_response("0400", "Mandatory fields need to be provided")
    if user_filter(data.get('email_id')):
        return error_response("0400",'User with this email or username already exists')
    hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    new_user = User(data.get('email_id'), data.get('first_name'), data.get('last_name'),
                        data.get('phone_number'), password=hashed_password)
    new_add(new_user)
    return success_response(201,"Success", "User created successfully")

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if check_user_required_fields(data):
       email_id = data.get('email_id')
       password = data.get('password')
       user = user_filter(email_id)
       if user and bcrypt.check_password_hash(user.password, password):
           access_token = create_access_token(identity=user.id)
           return jsonify({'access_token': access_token})
       else:
           return error_response('0400',' wrong email_id or password.')
    else:
        return error_response("0400",'Invalid email or password')

   
@bp.route('/information', methods=['GET'])
@jwt_required()
def get_data_by_id():
    user_id = get_jwt_identity()
    user =  user_filter_id(user_id)
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
    user = user_filter_id(user_id)
    if not user:
        return error_response("0404", 'User not found')  
    data = request.json
    phone_number = data.get('phone_number')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if not phone_number:
        if not first_name:
            if not last_name:
                return error_response("0400", 'invalid input')

    if phone_number:
        user.phone_number = phone_number
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    update_details()
    return success_response(200, "Success", "User details are updated successfully")


@bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = user_filter_id(user_id)
    if user:
        delete(user)
        return success_response(200, "Success", "Your profile is deleted")
    else:
        return error_response("0404",  'User not found')


@bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.json
    password = data.get('password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
    user = user_filter_id(user_id)
    if not user:
        return error_response("0404",  'User not found')
    if not bcrypt.check_password_hash(user.password, password):
        return error_response("0400", 'Incorrect password')
    if not new_password:
        return error_response("0400", 'New password not provided')
    if not confirm_new_password:
        return error_response("0400", 'Confirm_New password not provided')
    if confirm_new_password != new_password:
        return error_response("0400", 'Confirm_New password and new password field not match')
    else:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        update_details()
        return success_response(200, "Success", "Password changed successfully")



@bp.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.json
    email_id = data.get('email_id')
    user=user_filter(email_id)
    if not user:
         return error_response("0404",  'User not found')
    else:  
        expires = datetime.now() + timedelta(seconds=30)
        token = secrets.token_urlsafe(4)
        encoded_email_id  = base64.b64encode(email_id.encode('utf-8')).decode('utf-8')
        expires = base64.b64encode(str(expires).encode('utf-8')).decode('utf-8')
        reset_link = f'http://127.0.0.1:5000/reset_password{encoded_email_id}/{token}/{expires}'
        msg = Message( 'Hello', 
                sender=os.getenv('MAIL_USERNAME'),
                recipients=[email_id]) 
        msg.body =  f'Hello,\n\nYour reset code is/ {reset_link}'
        mail.send(msg)
        user.password_change_token = token
        update_details()
        return success_response(200, "Success", "The Mail is Send.")



@bp.route('/reset_password/<encoded_email_id>/<token>/<expires>', methods=['POST'])
def reset_password(encoded_email_id,token,expires):
    email_id = base64.b64decode(encoded_email_id).decode('utf-8') 
    expires = base64.b64decode(expires).decode('utf-8') 
    data = request.json
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')
    user = user_filter_token(email_id,token)
    print(user)
    current_time=datetime.now()
    expires = datetime.strptime(
    expires, '%Y-%m-%d %H:%M:%S.%f')
    if not user:
        return error_response("0404",  'User not found')
    if not new_password:
        return error_response("0400",  'New password not provided')
    if not confirm_new_password:
        return error_response("0400",  'Confirm_New password not provided')
    if confirm_new_password != new_password:
        return error_response("0400",  'Confirm_New password and new password field not match')
    if user and current_time<=expires:
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        user.password_change_token = None
        update_details()
        return success_response(200, "Success", "Password reset successfully")
    else:
        return  error_response("0400",  'Invalid token provided')

