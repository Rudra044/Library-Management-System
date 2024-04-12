from app.models.models import User, Passwordresettoken, db


def user_filter(email_id):
    return (User.query.filter_by(email_id=email_id).first())


def user_filter_id(user_id):
    return (User.query.filter_by(id=user_id).first())


def user_filter_token(user_id, token_encode):
    return (Passwordresettoken.query.filter(db.and_(Passwordresettoken.profile_id == user_id and Passwordresettoken.link == token_encode)).first())

def user_check(user_id):
    return(Passwordresettoken.query.filter_by(profile_id=user_id).first())
