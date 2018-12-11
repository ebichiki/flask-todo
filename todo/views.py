from flask import request, redirect, url_for, render_template, flash
from todo import app, db
from todo.models import Entry
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