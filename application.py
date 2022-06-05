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


@app.route('/api/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    authors = {a.id: f'{a.name} {a.city}' for a in authors}
    return authors




@app.route('/api/authors/create', methods=['POST'])
def create_author():
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


@app.route('/api/authors/delete/<id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get(id)
    if not author:
        return {"error": "NotFound"}
    db.session.delete(author)
    db.session.commit()
    return {"status": 200}


@app.route('/api/authors/update/<id>', methods=['PUT'])
def update_author(id):
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
