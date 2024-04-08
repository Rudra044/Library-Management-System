from app.models.models import User


def user_filter(email_id):
    return (User.query.filter_by(email_id=email_id).first())


def user_filter_id(user_id):
    return (User.query.filter_by(id=user_id).first())


