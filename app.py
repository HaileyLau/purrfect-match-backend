from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique = True, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(150), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/') # READ
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/data/<int:id>') # GET ROW
def get_data(id):
    cat = db.session.get(User, id)
    if cat:
        return jsonify(cat.to_dict())
    else:
        return jsonify({'error': 'no more cats'})



# def display_data():
#     with sqlite3.connect('data/data.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM CATS")
#         users = cursor.fetchall()
#         return users


# @app.route('/data') # display data
# def get_data():
#     data = display_data()
#     return render_template('index.html', users=data)


@app.route('/add', methods=['POST']) # CREATE
def add_user():
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']
    gender = request.form['gender']
    photo = request.form['photo']
    cat = User(name=name, breed=breed, age=age, gender=gender, photo=photo)
    db.session.add(cat)
    db.session.commit()
    return redirect(url_for('index'))

# def add_user():
#     name = request.form['name']
#     email = request.form['email']
#     user = User(name=name, email=email)
#     db.session.add(user)
#     db.session.commit()
#     return redirect(url_for('index'))



@app.route('/update', methods=['POST']) # UPDATE
def update_user():
    user_id = request.form['id']
    user = User.query.get(user_id)
    if user:
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>') # DELETE
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
