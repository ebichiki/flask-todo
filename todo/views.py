from flask import request, redirect, url_for, render_template, flash
from todo import app, db
from todo.models import Entry

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    format="%M:%S"
    return date.strftime(format) 

@app.route('/')
def show_entries():
    entries = Entry.query.order_by(Entry.id.asc()).all()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    entry = Entry(
            text=request.form['text'],
            complated=False
            )
    db.session.add(entry)
    db.session.commit()
    flash('Add a new task!')
    return redirect(url_for('show_entries'))

@app.route('/update/<int:id>', methods=['POST'])
def upd_entry(id):
    entry = Entry.query.get(id)
    if entry.complated == True:
        entry.complated = False
    else:
        entry.complated = True
    flash('Done!')
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