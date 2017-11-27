#!/usr/bin/python3
from flask import Flask, request
from flask import render_template
from flask import jsonify, make_response
import psycopg2
conn = psycopg2.connect(
    dbname= 'javier',
    user= 'javier',
    host= 'localhost',
    port= '5432'
    )


app = Flask(__name__)

@app.route('/')
def homepage():
    return """<h1>Hello Mate</h1>"""

@app.route('/monitoring-post', methods = ['POST'])
def datamanager():
    data = request.get_json(force=True)
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    user =  data.get("users")
    os = data.get('kernel')
    mem = data.get('mem free')
    swap = data.get('swap so')
    cpu = data.get('cpu sy')
    size = data.get('Disk Size')
    free = data.get('Free Disk Space')
    cur = conn.cursor()
    cur.execute("""INSERT INTO monitoring VALUES('"""+ time + """ ' , '""" + user + """ ' , '""" + os + """ ' , ' """
                 + mem + """  ' , ' """ + swap + """ ' , ' """ + cpu + """ ' , ' """ + size + """ ' , ' """
                 + free + """ ')""")
    cur.execute(""" COMMIT """)

    return "funca"

@app.route('/magnetlinks', methods = ['GET' , 'POST'])
def datamanagerm():
    if request.method == 'POST': ### cliente
        return "0"

    cur = conn.cursor()
    cur.execute("""SELECT url FROM magnetlinks """)
    rows = cur.fetchall()
    urls = {}
    x = 1
    for row in rows:
        urls['url'+ str(x)] = row[0]
        x += 1

    cur.execute("""DELETE FROM magnetlinks""")
    cur.execute(""" COMMIT """)

    return jsonify(urls)

@app.route('/status', methods = ['GET', 'POST'])
def status():
    if request.method == 'POST':
        data = request.get_json(force=True)
        cur = conn.cursor()
        name = data.get('name')
        progress = data.get('progress')
        ETA = data.get('ETA')
        status = data.get('status-1')
        speed = data.get('speeddown')

        cur.execute("""INSERT INTO downloads (name, progress, eta, status, speed) VALUES ('""" + name + """ ' , ' """
                    + progress + """ ' , ' """ + ETA + """ ' , ' """ + status + """ ' , ' """+ speed + """ ' """ )
        cur.execute("""COMMIT""")
        return "It works"





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port = 5001)
