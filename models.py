from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    poems = db.relationship('Poem', backref='book')
    contracts = db.relationship('Contract', backref='book')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    books = db.relationship('Book', backref='author')


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    text = db.Column(db.String(5000))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    addresses = db.relationship('Address', backref='publisher')
    contracts = db.relationship('Contract', backref='publisher')


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Boolean, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
