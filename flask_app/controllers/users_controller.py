from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models import user_model
from flask_app.models import show_model
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not user_model.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    session['user_id'] = user_model.User.register(data)
    return redirect('/')

@app.route('/login', methods = ["POST"])
def login():
    data = {"email": request.form['email']}
    user_in_db = user_model.User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "invalidlogin")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "invalidlogin")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/main")

@app.route("/main")
def main():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {'id': session['user_id']}
    
    return render_template('main.html', user=user_model.User.get_user_by_id(user_data), show_list = show_model.Show.view_all_shows(), creator = show_model.Show.show_creators())