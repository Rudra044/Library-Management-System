from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(250), unique=True, nullable=False)
    first_name = db.Column(db.String(250),  nullable=True)
    last_name=db.Column(db.String(250),  nullable=True)
    phone_number=db.Column(db.String(250), unique=True, nullable=True)
    password = db.Column(db.String(250), nullable=False)
    bookss = db.relationship('Books', backref='profile', cascade='all, delete')
    authors= db.relationship('Author', backref='profile', cascade='all, delete')


    def __init__(self, email_id, first_name, last_name, phone_number,password):
            self.email_id = email_id
            self.first_name = first_name
            self.last_name = last_name
            self.phone_number = phone_number
            self.password = password


class Books(db.Model):
      __tablename__ = "Books"
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(250), unique=True, nullable=False)
      author = db.Column(db.String(250), nullable=False)
      isbn = db.Column(db.String(250),  nullable=False)
      genre = db.Column(db.String(250),  nullable=True)
      publication_year =  db.Column(db.Integer,  nullable=False)
      profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

      def __init__(self, title,  author, isbn, genre,publication_year,profile_id):
            self.title = title
            self.author =  author
            self.isbn = isbn
            self.genre = genre
            self.publication_year= publication_year
            self.profile_id= profile_id

class Author(db.Model):
      __tablename__= "Author"
      id = db.Column(db.Integer, primary_key=True)
      author_name= db.Column(db.String(250), nullable=False)
      biography = db.Column(db.String(5000), nullable=False)
      nationality = db.Column(db.String(250),  nullable=False)
      profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))


      def __init__(self,author_name,biography,nationality,profile_id):
            self.author_name = author_name
            self.biography =  biography
            self.nationality = nationality
            self.profile_id=profile_id


            