from app.models.models import db


def new_add(new):
    db.session.add(new)
    db.session.commit()


def delete(info):
    db.session.delete(info)
    db.session.commit() 


def update_details():
    db.session.commit()

