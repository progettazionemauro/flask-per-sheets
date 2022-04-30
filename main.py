from flask import Flask, render_template, request, url_for, flash, redirect

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
    'price': 34,
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

@app.route('/course/', methods=('GET', 'POST'))
def course():
    form = CourseForm()
    return render_template('course.html', form=form)



  
  


app.run(host='0.0.0.0', port=8080, debug=True)
