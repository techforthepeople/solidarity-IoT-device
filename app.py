from flask import Flask, flash, render_template, request, redirect, session, url_for
import uuid
import sqlite3
from sqlite3 import Error
from marshmallow import Schema, fields

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

db = app.config["DB_NAME"]

def create_connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except Error as e:
        print(e)

    return con

@app.route('/')
def index():

    # fetch current settings from db
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

    # render configuration page with current settings
    return render_template('index.html', settings = current_settings)


# set validation rules for settings
class UpdateSettingsInputSchema(Schema):
    userid = fields.Str(required=True)
    high_temp = fields.Int(required=True)
    low_temp = fields.Int(required=True)
    high_humidity = fields.Int(required=True)
    low_humidity = fields.Int(required=True)
    high_pressure = fields.Int(required=True)
    low_pressure = fields.Int(required=True)
    polling_frequency = fields.Int(required=True)

@app.route('/update_settings', methods=['POST'])
def update_settings():

    if request.method == 'POST':

        # check for validation errors
        update_settings_schema = UpdateSettingsInputSchema()
        errors = update_settings_schema.validate(request.form)
        if errors:
            flash(errors)
            return redirect(url_for('index'))
        
        # get setting values from form data
        userid = request.form.get('userid')
        high_temp = request.form.get('high_temp')
        low_temp = request.form.get('low_temp')
        high_humidity = request.form.get('high_humidity')
        low_humidity = request.form.get('low_humidity')
        high_pressure = request.form.get('high_pressure')
        low_pressure = request.form.get('low_pressure')
        polling_frequency = request.form.get('polling_frequency')

        # clear existing settings in db
        con = create_connection(db)
        cur = con.cursor()
        cur.execute('DELETE from settings')
        con.commit()

        # insert the updated settings into db
        sql = 'INSERT INTO settings (userid,low_temp,high_temp,low_humidity,high_humidity,low_pressure,high_pressure,polling_frequency) VALUES (?,?,?,?,?,?,?,?)'
        cur.execute(sql, (userid, low_temp, high_temp, low_humidity,
                          high_humidity, low_pressure, high_pressure, polling_frequency))
        con.commit()

        flash('Updated settings.')
        return redirect(url_for('index'))

      
if __name__ == '__main__':
    app.run(host='0.0.0.0')
