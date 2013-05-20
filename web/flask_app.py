from flask import Flask,render_template
from flask.ext.bootstrap import Bootstrap
import sqlite3


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index(rows=None):
    conn = sqlite3.connect('/home/pallih/x13/db/db.sqlite')
    cur = conn.cursor()
    cur.execute('''
        SELECT * from questions ORDER BY id
        ''')
    rows = cur.fetchall()
    return render_template('index.html',rows=rows)


@app.route('/um')
def um():
    return render_template('about.html')


@app.route('/spurning/<int:id>')
def spurning(id):
    conn = sqlite3.connect('/home/pallih/x13/db/db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' ORDER BY candidates.party')
    rows = cur.fetchall()
    cur.execute('SELECT * from questions WHERE id = '+str(id))
    question = cur.fetchall()
    question_text = question[0][0]
    question_id = question[0][1]
    options = []
    for row in rows:
        options.append(row[2])
    answer_options = set(options)
    districts = []
    for row in rows:
        districts.append(row[4])
    districts = set(districts)
    return render_template('spurning.html', rows=rows, question_text=question_text,
        question_id=question_id,answer_options=answer_options,districts=districts)


@app.route('/spurning/<int:id>/<district>')
def spurning_district(id, district):
    conn = sqlite3.connect('/home/pallih/x13/db/db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' ORDER BY candidates.party')
    districts = cur.fetchall()
    cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' AND candidates.district LIKE "'+district+'" ORDER BY candidates.party')
    rows = cur.fetchall()
    cur.execute('SELECT * from questions WHERE id = '+str(id))
    question = cur.fetchall()
    question_text = question[0][0]
    question_id = question[0][1]
    options = []
    for row in rows:
        options.append(row[2])
    answer_options = set(options)
    districts_return = []
    for row in districts:
        districts_return.append(row[4])
    districts = set(districts_return)
    district_selected = district
    return render_template('spurning_district.html', rows=rows, question_text=question_text,
        question_id=question_id,answer_options=answer_options,districts=districts,district_selected=district_selected)


@app.route('/spurning/<int:id>/frambjodendur/saeti/<place>')
def spurning_candidate_place(id, place):
    conn = sqlite3.connect('/home/pallih/x13/db/db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' ORDER BY candidates.party')
    districts = cur.fetchall()
    if place == "1":
        cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' AND candidates.candidate_placement = 1 ORDER BY candidates.party')
        rows = cur.fetchall()
    if place == "1-3":
        cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' AND candidates.candidate_placement in (1,2,3) ORDER BY candidates.candidate_placement')
        rows = cur.fetchall()
    if place == "1-5":
        cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' ORDER BY candidates.party')
        rows = cur.fetchall()
    cur.execute('SELECT * from questions WHERE id = '+str(id))
    question = cur.fetchall()
    question_text = question[0][0]
    question_id = question[0][1]
    options = []
    for row in rows:
        options.append(row[2])
    answer_options = set(options)
    districts_return = []
    for row in districts:
        districts_return.append(row[4])
    districts = set(districts_return)
    place_selected = place
    return render_template('spurning_district.html', rows=rows, question_text=question_text,
        question_id=question_id,answer_options=answer_options,districts=districts, place_selected=place_selected)


@app.route('/spurning/<int:id>/frambjodendur/saeti/<place>/<district>')
def spurning_candidate_place_district(id, place, district):
    conn = sqlite3.connect('/home/pallih/x13/db/db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' ORDER BY candidates.party')
    districts = cur.fetchall()
    if place == "1":
        cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' AND candidates.candidate_placement = 1 AND candidates.district LIKE "'+district+'" ORDER BY candidates.party')
        rows = cur.fetchall()
    if place == "1-3":
        cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' AND candidates.candidate_placement in (1,2,3) AND candidates.district LIKE "'+district+'" ORDER BY candidates.candidate_placement')
        rows = cur.fetchall()
    if place == "1-5":
        cur.execute('SELECT * FROM question_responses JOIN candidates ON question_responses.candidate_name = candidates.candidate_name WHERE question_responses.q_id = '+str(id)+' AND candidates.district LIKE "'+district+'" ORDER BY candidates.party')
        rows = cur.fetchall()
    cur.execute('SELECT * from questions WHERE id = '+str(id))
    question = cur.fetchall()
    question_text = question[0][0]
    question_id = question[0][1]
    options = []
    for row in rows:
        options.append(row[2])
    answer_options = set(options)
    districts_return = []
    for row in districts:
        districts_return.append(row[4])
    districts = set(districts_return)
    place_selected = place
    district_selected = district
    return render_template('spurning_district.html', rows=rows, question_text=question_text,
        question_id=question_id,answer_options=answer_options,districts=districts, place_selected=place_selected,district_selected=district_selected)

