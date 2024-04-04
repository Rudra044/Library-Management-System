from flask import Flask, request, jsonify
from flask_migrate import Migrate
from app.models.models import  db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from urllib.parse import unquote_plus, quote_plus
from config import Config
import os

bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)


    from app.api import user, book, author
    app.register_blueprint(user.bp)
    app.register_blueprint(book.bp)
    app.register_blueprint(author.bp)





    return app