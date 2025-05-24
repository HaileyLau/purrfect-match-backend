from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/') # READ
def index():
    users = Cat.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST']) # CREATE
def add_user():
    name = request.form['name']
    breed = request.form['breed']
    age = request.form['age']
    gender = request.form['gender']
    photo = request.form['photo']
    cat = Cat(name=name, breed=breed, age=age, gender=gender, photo=photo)
    db.session.add(cat)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST']) # UPDATE
def update_user():
    user_id = request.form['id']
    user = Cat.query.get(user_id)
    if user:
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>') # DELETE
def delete_user(id):
    user = Cat.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)