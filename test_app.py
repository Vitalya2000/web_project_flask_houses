import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

'''conn = psycopg2.connect(database="houses", user="postgres",
                        password="postgres", host="localhost", port="5432")
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS hr_houses;')
cur.execute('CREATE TABLE hr_houses (id serial PRIMARY KEY,'
            'address varchar (150) NOT NULL,'
            'district varchar (75) NOT NULL,'
            'type varchar (20) NOT NULL,'
            'quan_of_floors integer NOT NULL,'
            'quan_of_entrances integer NOT NULL,'
            'date_of_construction text NOT NULL,'
            'date_of_destruction text NOT NULL,'
            'photo text,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )
cur.execute(INSERT INTO hr_houses (address, district, type, quan_of_floors, quan_of_entrances, 
date_of_construction, date_of_destruction, photo) VALUES (' Проезд Дежнёва д.8', 'СВАО, район Южное Медведково', 
'К-7-3-4', 5, 4, '1964', '09-2017', 'http://photos.wikimapia.org/p/00/02/78/61/39_1280.jpg');
            ) 
conn.commit()
cur.close()
conn.close()'''


@app.route('/')
def index():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM hr_houses ORDER BY id ASC;''')
    houses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', houses=houses)


@app.route('/tools')
def tools():
    return render_template('tools.html')


@app.route('/tools/res_ent', methods=['POST'])
def select_entrances():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    quan_of_entrances = request.form['quan_of_entrances']
    cur.execute('''SELECT * FROM hr_houses WHERE quan_of_entrances=%s ORDER BY id ASC''', (quan_of_entrances,))
    houses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('result.html', houses=houses)


@app.route('/tools/search_address', methods=['POST'])
def select_address():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    address = request.form['address']
    cur.execute("SELECT * FROM hr_houses WHERE address LIKE'%" + address + "%' ORDER BY id ASC;")
    houses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('result.html', houses=houses)


@app.route('/tools/search_district', methods=['POST'])
def select_district():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    district = request.form['district']
    cur.execute("SELECT * FROM hr_houses WHERE district LIKE'%" + district + "%' ORDER BY id ASC;")
    houses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('result.html', houses=houses)


@app.route('/tools/search_type', methods=['POST'])
def select_type():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    h_type = request.form['type']
    cur.execute("SELECT * FROM hr_houses WHERE type LIKE'%" + h_type + "%' ORDER BY id ASC;")
    houses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('result.html', houses=houses)


@app.route('/tools/create', methods=['POST'])
def create():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    address = request.form['address']
    district = request.form['district']
    h_type = request.form['type']
    quan_of_floors = request.form['quan_of_floors']
    quan_of_entrances = request.form['quan_of_entrances']
    date_of_construction = request.form['date_of_construction']
    date_of_destruction = request.form['date_of_destruction']
    photo = request.form['photo']
    cur.execute(
        '''INSERT INTO hr_houses (address, district, type, quan_of_floors, quan_of_entrances, 
date_of_construction, date_of_destruction, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
        (address, district, h_type, quan_of_floors, quan_of_entrances,
         date_of_construction, date_of_destruction, photo))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('update'))


@app.route('/tools/update', methods=['POST'])
def update():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    address = request.form['address']
    district = request.form['district']
    h_type = request.form['type']
    quan_of_floors = request.form['quan_of_floors']
    quan_of_entrances = request.form['quan_of_entrances']
    date_of_construction = request.form['date_of_construction']
    date_of_destruction = request.form['date_of_destruction']
    photo = request.form['photo']
    h_id = request.form['id']
    cur.execute(
        '''UPDATE hr_houses SET address=%s, district=%s, type=%s, quan_of_floors=%s, quan_of_entrances=%s, 
date_of_construction=%s, date_of_destruction=%s, photo=%s WHERE id=%s''',
        (address, district, h_type, quan_of_floors, quan_of_entrances,
         date_of_construction, date_of_destruction, photo, h_id))
    conn.commit()
    return redirect(url_for('update'))


@app.route('/delete', methods=['POST'])
def delete():
    conn = psycopg2.connect(database="houses", user="postgres", password="postgres", host="localhost", port="5432")
    cur = conn.cursor()
    h_id = request.form['id']
    cur.execute("DELETE FROM hr_houses WHERE id = {}".format(h_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))


@app.route('/tools/delete', methods=['POST'])
def modify_delete():
    conn = psycopg2.connect(database="houses", user="postgres", password="postgres", host="localhost", port="5432")
    cur = conn.cursor()
    h_id = request.form['id']
    cur.execute("DELETE FROM hr_houses WHERE id = {}".format(h_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('update'))


@app.route('/tools/update')
def modify():
    conn = psycopg2.connect(database="houses",
                            user="postgres",
                            password="postgres",
                            host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute('''SELECT * FROM hr_houses ORDER BY id ASC;''')
    houses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('update.html', houses=houses)


@app.route('/')
def back_to_main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
