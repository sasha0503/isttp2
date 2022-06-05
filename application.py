from json import JSONDecodeError

from flask import Flask, request, render_template

import jsonpickle

from models import *


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.app_context().push()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books = {b.id: f'{b.name} {b.year}' for b in books}
    return books


@app.route('/api/books/create', methods=['POST'])
def create_book():
    r = request
    try:
        data: dict = jsonpickle.decode(r.data)
    except JSONDecodeError:
        return {"status": 500}
    book = Book(name=data['name'], year=data['year'], author=data['author'])
    db.session.add(book)
    db.session.commit()
    return {"id": book.id}


@app.route('/api/books/delete/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return {"status": 404}
    db.session.delete(book)
    db.session.commit()
    return {"status": 200}


@app.route('/api/books/update/<id>', methods=['PUT'])
def update_book(id):
    r = request
    try:
        data: dict = jsonpickle.decode(r.data)
    except JSONDecodeError:
        return {"status": 500}
    book = Book.query.get(id)
    if not book:
        return {"status": 404}
    book.name = data.get('name', book.name)
    book.year = data.get('year', book.year)
    book.author = data.get('author', book.author)
    db.session.commit()
    return {"status": 200}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
