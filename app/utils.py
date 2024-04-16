import os,base64

from flask_mail import Message
from cryptography.fernet import Fernet

from app import mail
from app.models.models import db


fernet_key = Fernet.generate_key()
cipher = Fernet(fernet_key)


def new_add(new):
    db.session.add(new)
    db.session.commit()


def delete(info):
    db.session.delete(info)
    db.session.commit() 


def update_details():
    db.session.commit()


def send_mail(email_id,reset_link):   
                    msg = Message( 'Hello', 
                    sender = os.getenv('MAIL_USERNAME'),
                    recipients = [email_id]) 
                    msg.body =  f'Hello,\n\nYour reset code is/ {reset_link}'
                    mail.send(msg)


def encrypt_with_secret_key(data):
    data_bytes = data.encode('utf-8')
    encrypted_data = cipher.encrypt(data_bytes)
    print('hdhf',encrypted_data)
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')


def decrypt_with_secret_key(encoded_data):
    encrypted_data = base64.urlsafe_b64decode(encoded_data.encode('utf-8'))
    print('hdhf',encrypted_data)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data.decode('utf-8')

