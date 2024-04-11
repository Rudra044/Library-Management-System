from app.models.models import User, db


def user_filter(email_id):
    return (User.query.filter_by(email_id=email_id).first())


def user_filter_id(user_id):
    return (User.query.filter_by(id=user_id).first())

def user_filter_token(email_id,token):
    return (User.query.filter(db.and_(User.email_id==email_id and User.password_change_token == token)).first())


