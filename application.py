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
app.jinja_env.filters['zip'] = zip


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/authors', methods=['GET'])
def get_authors_api():
    authors = Author.query.all()
    authors = {a.id: f'{a.name} {a.city}' for a in authors}
    return authors


@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    names = [a.name for a in authors]
    ids = [a.id for a in authors]
    return render_template('authors.html', names=names, ids=ids)


@app.route('/authors/<id>', methods=['GET'])
def get_author(id):
    author = Author.query.get(id)
    name = author.name
    city = author.city
    books = author.books
    return render_template('author.html', name=name, city=city, books=books)


@app.route('/publishers', methods=['GET'])
def get_pubs():
    pubs = Publisher.query.all()
    names = [a.name for a in pubs]
    ids = [a.id for a in pubs]
    return render_template('common_view.html', names=names, ids=ids, category="publishers")


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    names = [a.name for a in books]
    ids = [a.id for a in books]
    return render_template('common_view.html', names=names, ids=ids, category="books")


@app.route('/api/authors/create', methods=['POST'])
def create_author_api():
    r = request
    try:
        data: dict = jsonpickle.decode(r.data)
    except JSONDecodeError:
        return {"error": "BadJSON"}
    try:
        name = data['name']
        city = data['city']
    except KeyError:
        return {"error": "InputError"}
    author = Author(name=name, city=city)
    db.session.add(author)
    db.session.commit()
    return {"id": author.id}


@app.route('/authors/create', methods=['POST'])
def create_author():
    r = request
    try:
        name = r.form['name']
        city = r.form['city']
    except KeyError:
        return {"error": "InputError"}
    author_old = Author.query.filter_by(name=name).first()
    if author_old:
        return render_template("error.html", error_text="Такий автор уже є")
    author = Author(name=name, city=city)
    db.session.add(author)
    db.session.commit()
    authors = Author.query.all()
    names = [a.name for a in authors]
    ids = [a.id for a in authors]
    return render_template('authors.html', names=names, ids=ids)


def delete_workarround(name):
    author = Author.query.filter_by(name=name).first()
    if not author:
        return render_template("error.html", error_text="Такого автора немає")
    db.session.delete(author)
    db.session.commit()


@app.route('/authors/delete', methods=['POST'])
def delete_author():
    r = request
    try:
        name = r.form['name']
    except KeyError:
        return {"error": "InputError"}
    delete_workarround(name)
    authors = Author.query.all()
    names = [a.name for a in authors]
    ids = [a.id for a in authors]
    return render_template('authors.html', names=names, ids=ids)


def update_workarround(name, new_name, new_city):
    author = Author.query.filter_by(name=name).first()
    if not author:
        return render_template("error.html", error_text="Такого автора немає")
    new_authors = [i for i in Author.query.filter_by(name=new_name)]
    for i in new_authors:
        if i.id != author.id:
            return render_template("error.html", error_text="Такий автор уже є")
    author.city = new_city
    author.name = new_name
    db.session.commit()


@app.route('/authors/update', methods=['POST'])
def update_author():
    r = request
    try:
        name = r.form['name']
        new_name = r.form['new_name']
        new_city = r.form['new_city']
    except KeyError:
        return {"error": "InputError"}
    update_workarround(name, new_name, new_city)
    authors = Author.query.all()
    names = [a.name for a in authors]
    ids = [a.id for a in authors]
    return render_template('authors.html', names=names, ids=ids)


@app.route('/api/authors/delete/<id>', methods=['DELETE'])
def delete_author_api(id):
    author = Author.query.get(id)
    if not author:
        return {"error": "NotFound"}
    db.session.delete(author)
    db.session.commit()
    return {"status": 200}


@app.route('/api/authors/update/<id>', methods=['PUT'])
def update_author_api(id):
    r = request
    try:
        data: dict = jsonpickle.decode(r.data)
    except JSONDecodeError:
        return {"error": "BadJSON"}
    author = Author.query.get(id)
    if not author:
        return {"error": "NotFound"}
    author.name = data.get('name', author.name)
    author.city = data.get('city', author.city)
    db.session.commit()
    return {"status": 200}


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
