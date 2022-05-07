from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3

from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img
import gspread
from forms import CourseForm

app = Flask('app')
app.config['SECRET_KEY'] = 'abc'

courses_list = [{
    'title': 'Python 101',
    'description': 'Learn Python basics',
    'Price': 34,
    'available': True,
    'level': 'Beginner'
    }]


dati = [{
    'title': 'Messaggio UNO',
    'content': 'Message One Content'
}, {
    'title': 'Messaggio DUE',
    'content': 'Message Two Content'
}]
sa = gspread.service_account(filename='./service_account.json')
sh = sa.open("Copia di opensheet test")

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
  
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
  

@app.route('/databasevista/')
def data_base():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('databasevista.html', posts=posts)

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('data_base'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('data_base'))
  
@app.route('/databasecrea/', methods=('GET', 'POST'))
def create_messaggio():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('data_base'))

    return render_template('databasecrea.html')

# @app.route('/')
# def index1():
# fin qui: vedere TUT https://www.youtube.com/watch?v=bu5wXjz2KvU
# wks = sh.worksheet("Test Sheet")
# print('Rows:', wks.row_count)
# print('Columns:', wks.col_count)
# print('Valore:', wks.acell('B5').value)
# print('Valore:', wks.cell(5,2).value)
# print('Valore:', wks.get('B1:C8'))
# print('Valore:', wks.get_all_records())
# wks.update('B5', 'Mauro ha vinto!!')
# wks.update('B5:B7', [['[Mauro'],[Giovanni']])
# wks.update('F2','=UPPER(B2)', raw=False)
# wks.delete_columns(3)
# data = wks.get_all_values()
# for i in range(len(data)):
#    if i == 0:
#        continue
#   else:
#        data[i][1]
#return render_template('index.html', data=data[1:]) """
@app.route('/')
# inserimento in tabella
def hello_world():
    wks = sh.worksheet("Test Sheet")
    data = wks.get_all_values()
    for i in range(len(data)):
        if i == 0:
            continue
        else:
            data[i][1]
    return render_template('index1.html', data=data[1:])


@app.route('/dropdown/', methods=('GET', 'POST'))
# inserimento in tabella OPERAZIONE GET
def drop_list():
    wks = sh.worksheet("Test Sheet")
    data = wks.get_all_values()
    for i in range(len(data)):
        if i == 0:
            continue
        else:
            data[i][1]
    return render_template('dropdown.html', data=data[1:])
# VEDERE QUESTO TUT: https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf
@app.route('/course/', methods=('GET', 'POST'))
def course():
    form = CourseForm()
    if form.validate_on_submit():
        courses_list.append({'title': form.title.data,
                             'description': form.description.data,
                             'price': form.price.data,
                             'available': form.available.data,
                             'level': form.level.data
                             })
        return redirect(url_for('course'))



  
    return render_template('course.html', form=form)



  
  


app.run(host='0.0.0.0', port=8080, debug=True)
