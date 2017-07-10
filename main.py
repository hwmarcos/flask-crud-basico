from flask import Flask, request, jsonify, render_template, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="public")

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1234@localhost/flask"
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(120))
  password = db.Column(db.String(120))

  def __init__(self, username, password):
    self.username = username
    self.password = password


@app.route('/', methods = ['GET'])
def hello():
  users = User.query.all()
  json_users = []
  for user in users:
    obj = {
        'username': user.username,
        'password': user.password
    }

    json_users.append(obj)

  return jsonify(users = json_users)

@app.route('/create', methods = ['POST'])
def create():
  user = User(request.form['username'], request.form['password'])

  db.session.add(user)
  db.session.commit()

  obj = {
    'username' : request.form['username'],
    'password' : request.form['password']
  } 

  return jsonify(user = obj)


@app.route('/delete/<int:id>', methods = ['DELETE', 'POST'])
def delete(id):
  user = User.query.get(id)

  db.session.delete(user)
  db.session.commit()

  obj = {
    'id' : user.id
  }

  return jsonify(user = id)


@app.route('/edit/<int:id>', methods = ['PUT', 'POST', 'PATCH'])
def update(id):
  user = User.query.get(id)

  user.username = request.form['username']
  user.password = request.form['password']

  db.session.commit()

  obj = {
    'username': user.username,
    'password': user.password
  }

  return jsonify(user = obj)

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

