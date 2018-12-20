from functools import wraps
from flask import request, redirect, url_for, render_template, flash, abort, jsonify, session, g
from todo import app, db
from todo.models import Entry, User
from datetime import datetime

starttime = datetime.now()
status = ["Start","Done!","Clear"]

@app.template_filter('strftime')
def _jinja2_filter_datetime(entry):
    delta = entry.updated_at - entry.created_at
    return str(delta).split(".")[0]
    
@app.template_filter('btnnm')
def _jinja2_filter_datetime(arg):
    return status[arg]

# def login_required(f):
#     @wraps(f)
#     def decorated_view(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for('login', next=request.path))
#         return f(*args, **kwargs)
#     return decorated_view
#
# @app.before_request
# def load_user():
#     user_id = session.get('user_id')
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.get(session['user_id'])

@app.route('/')
def show_entries():
    entries = Entry.query.order_by(Entry.id.asc()).all()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    entry = Entry(
            text=request.form['text'],
            completed=0
            )
    db.session.add(entry)
    db.session.commit()
    flash('Add a new task!')
    return redirect(url_for('show_entries'))

@app.route('/update/<int:id>', methods=['POST'])
def upd_entry(id):
    #global starttime
    entry = Entry.query.get(id)
    if entry.completed == 0:
        entry.created_at = datetime.now()
        entry.completed = 1
        flash('Start!')
    elif entry.completed == 1:
        entry.updated_at = datetime.now()
        entry.completed = 2
        flash('Done!')
    else:
        print(2)
        entry.completed = 0
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for('show_entries'))

@app.route('/delete/<int:id>', methods=['POST'])
def del_entry(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('Delete a task!')
    return redirect(url_for('show_entries'))

@app.route('/users/')
def user_list():
    users = User.query.all()
    return render_template('user/list.html', users=users)

@app.route('/users/<int:user_id>/')
def user_detail(user_id):
    user = User.query.get(user_id)
    return render_template('user/detail.html', user=user)

@app.route('/users/<int:user_id>/edit/', methods=['GET', 'POST'])
def user_edit(user_id):
    user = User.query.get(user_id)
    if user is None:
        abort(404)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_detail', user_id=user_id))
    return render_template('user/edit.html', user=user)

@app.route('/users/create/', methods=['GET','POST'])
def user_create():
    if request.method == 'POST':
        user = User(name=request.form['name'],
                    email=request.form['email'],
                    password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_list'))
    return render_template('user/edit.html')

@app.route('/users/<int:user_id>/delete/', methods=['DELETE'])
def user_delete(user_id):
    user = User.query.get(user_id)
    if user is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'OK'})

@app.route('/login', methods={'GET', 'POST'})
def login():
    if request.method == 'POST':
        user, authenticated = User.authenticate(db.session.query,
                                                request.form['email'], request.form['password'])
        if authenticated:
            session['user_id'] = user.id
            flash('login')
            return redirect(url_for('show_entries'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('logout')
    return redirect(url_for('show_entries'))

