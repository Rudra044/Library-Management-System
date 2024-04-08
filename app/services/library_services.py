from app.models.models import Books, Author, db 

def book_filter(user_id,title,author):
    return(Books.query.filter(db.and_(Books.profile_id == user_id, Books.title == title, Books.author == author)).first())


def book_id_filter(user_id,book_id):
    return( Books.query.filter(db.and_(Books.profile_id == user_id, Books.id == book_id)).first())


def book_get(book_id):
    return (Books.query.get(book_id))


def book_all():
    return(Books.query.all())


def author_filter(user_id, author_name, biography):
    return(Author.query.filter(db.and_(Author.profile_id == user_id, Author.author_name == author_name 
                                    , Author.biography == biography)).first())


def author_id_all_filter(user_id):
    return(Author.query.filter(Author.profile_id == user_id).all())

def author_id_filter(user_id, author_id):
    return(Author.query.filter(db.and_(Author.profile_id == user_id, Author.id == author_id)).first())


def author_all():
    return(Author.query.all())


def author_get(author_id):
    return(Author.query.get(author_id))