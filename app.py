from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

db = 'sensor.db'

def create_connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except Error as e:
        print(e)

    return con


@app.route('/')
def index():
    con = create_connection(db)
    cur = con.cursor()
    cur.execute('SELECT * FROM settings')
    results = cur.fetchone()

    current_settings = {}
    if results is not None:
        current_settings = {
            'userid': results[0],
            'low_temp': results[1],
            'high_temp': results[2],
            'low_humidity': results[3],
            'high_humidity': results[4],
            'low_pressure': results[5],
            'high_pressure': results[6],
            'polling_frequency': results[7]
        }

    return render_template('index.html', settings = current_settings)


@app.route('/update_settings', methods=['POST', 'GET'])
def update_settings():
    if request.method == 'GET':
        userid = request.values.get('userid')
        high_temp = int(request.values.get('high_temp'))
        low_temp = int(request.values.get('low_temp'))
        high_humidity = int(request.values.get('high_humidity'))
        low_humidity = int(request.values.get('low_humidity'))
        high_pressure = int(request.values.get('high_pressure'))
        low_pressure = int(request.values.get('low_pressure'))
        polling_frequency = int(request.values.get('polling_frequency'))

        con = create_connection(db)

        # clear existing settings
        cur = con.cursor()
        cur.execute('DELETE from settings')
        con.commit()

        # insert the updated settings
        sql = 'INSERT INTO settings (userid,low_temp,high_temp,low_humidity,high_humidity,low_pressure,high_pressure,polling_frequency) VALUES (?,?,?,?,?,?,?,?)'
        cur.execute(sql, (userid, low_temp, high_temp, low_humidity,
                          high_humidity, low_pressure, high_pressure, polling_frequency))
        con.commit()

        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
