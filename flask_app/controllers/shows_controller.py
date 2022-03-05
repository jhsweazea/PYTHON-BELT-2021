from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models import user_model
from flask_app.models import show_model

@app.route('/new/show')
def new_show():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id":session['user_id']
    }
    return render_template('new_show.html', user = user_model.User.get_user_by_id(data))

@app.route('/addshow', methods = ['POST'])
def add_show():
    if 'user_id' not in session:
        return redirect('/')
    if not show_model.Show.validate_show_info(request.form):
        return redirect('/new/show')
    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
        "creator_id": session['user_id']
    }
    show_model.Show.add_show(data)
    return redirect('/main')

@app.route('/view/show/<int:id>')
def view_show(id):
    if 'user_id' not in session:
        return redirect('logout')
    data = {"id": id}
    user_data = {'id': session['user_id']}
    return render_template("view_show.html", show = show_model.Show.view_show_by_id(data), user=user_model.User.get_user_by_id(user_data), creator = show_model.Show.show_creator_by_id(data))

@app.route('/edit/show/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('logout')
    data = {'id': id}
    user_data = {'id': session['user_id']}
    return render_template("edit_show.html", show = show_model.Show.view_show_by_id(data), user=user_model.User.get_user_by_id(user_data))

@app.route('/update/show', methods=['POST'])
def update_show():
    if 'user_id' not in session:
        return redirect('logout')
    if not show_model.Show.validate_show_info(request.form):
        return redirect('/main')
    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['release_date'],
        "description": request.form['description'],
        "creator_id": session['user_id']
    }
    show_model.Show.update(data)
    return redirect('/main')

@app.route('/delete/show/<int:id>')
def delete_show(id):
    if 'user_id' not in session:
        return redirect('logout')
    data = {'id': id}
    show_model.Show.delete(data)
    return redirect("/main")

@app.route('/logout')
def logout():
    session.pop("user_id")
    return redirect('/')