from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlite3 import Error
from marshmallow import Schema, fields

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


class UpdateSettingsInputSchema(Schema):
    userid = fields.Str(required=False)
    high_temp = fields.Int(required=True)
    low_temp = fields.Int(required=True)
    high_humidity = fields.Int(required=True)
    low_humidity = fields.Int(required=True)
    high_pressure = fields.Int(required=True)
    low_pressure = fields.Int(required=True)
    polling_frequency = fields.Int(required=True)

update_settings_schema = UpdateSettingsInputSchema()

@app.route('/update_settings', methods=['POST'])
def update_settings():
    if request.method == 'POST':
        errors = update_settings_schema.validate(request.form)
        if errors:
            return render_template('results.html', msg=str(errors))

        userid = request.form.get('userid')
        high_temp = request.form.get('high_temp')
        low_temp = request.form.get('low_temp')
        high_humidity = request.form.get('high_humidity')
        low_humidity = request.form.get('low_humidity')
        high_pressure = request.form.get('high_pressure')
        low_pressure = request.form.get('low_pressure')
        polling_frequency = request.form.get('polling_frequency')

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

        return render_template('results.html', msg='Settings were updated successfully.')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
