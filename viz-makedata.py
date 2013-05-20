# encoding=utf-8

# import simplejson as json
import json
import sqlite3 as db
from datetime import datetime

payload = {}
questions = []
population = []

lookup_q = {}
with open("data/dv_questions.json", 'r') as f:
  s = f.read()
  questions = json.loads( s )

  for q in questions:
    _id = q['id']
    q['id'] = q['name']
    del q['name']
    lookup_q[ _id ] = q

    # ensure choices are id'ed
    for i, c in enumerate(q['choices']):
      c['id'] = str(i+1)



with db.connect('data/db.sqlite') as connection:
  cursor = connection.cursor()

  # add party to questions
  cursor.execute( 'SELECT DISTINCT party FROM candidates' )
  parties = cursor.fetchall()
  questions.insert(0,{
    "id": "party",
    "title": u"Stjórnmálaflokkur",
    "short": u"Stjórnmálaflokkur",
    "choices": [{
      'id': str(i+1),
      'title': p[0]
    } for i, p in enumerate(parties)]
  })

  cursor.execute( 'SELECT district, party, candidate_placement, candidate_name, done FROM candidates' )
  candidates = cursor.fetchall()
  for c in candidates:
    cand = {
              'locale': c[0],
              'party': c[1],
              'seat': int(c[2]),
              'name': c[3],
              '_answered': c[4] == 1
            }
    cursor.execute( 'SELECT q_id, response FROM question_responses WHERE candidate_name = "%s"' % c[3] )
    for r in cursor.fetchall():
      q = lookup_q[ str(r[0]) ]
      cand[ q['id'] ] = r[1]

    population.append( cand )


payload['questions'] = questions
payload['population'] = population
payload['buildtime'] = datetime.now().isoformat()


with open("dist/data.json", 'w+') as f:
  f.write( json.dumps( payload, indent=0, ensure_ascii=False ).encode( 'utf-8' ) )

