from sense_hat import SenseHat
import json
import time
from datetime import datetime as dt
import requests
import os
import sqlite3
from sqlite3 import Error
import requests

sense = SenseHat()

# config
db = 'sensor.db'
api_url = 'api_url_goes_here'

def sleep(x):
    return time.sleep(x / 1000.0)

# connect to database
def create_connection(db):
    con = None
    try:
        con = sqlite3.connect(db)
    except Error as e:
        print(e)

    return con


# get settings from database
def get_settings():
    con = create_connection(db)
    cur = con.cursor()
    cur.execute('SELECT * FROM settings')
    results = cur.fetchone()
    settings = None
    if results is not None:
        settings = {
            'userid': results[0],
            'low_temp': results[1],
            'high_temp': results[2],
            'low_humidity': results[3],
            'high_humidity': results[4],
            'low_pressure': results[5],
            'high_pressure': results[6],
            'polling_frequency': results[7]
        }
    return settings


def safe():
    sense.show_message('OK', text_colour=[255, 255, 255], back_colour=[0, 255, 0])


def unsafe():
    os.system('omxplayer warning.mp3')
    sense.show_message('UNSAFE', text_colour=[255, 255, 255], back_colour=[255, 0, 0])


def main():
    settings = get_settings()

    if settings is not None:
        print('Settings: ', settings)

        while True:

            temp = sense.get_temperature()
            humidity = sense.get_humidity()
            pressure = sense.get_pressure()

            # format and send data to backend
            data = {
                'authId': settings['userid'],
                'timeLogged': dt.now(),
                'temp': temp,
                'humidity': humidity,
                'pressure': pressure
            }

            try:
                r = requests.post(api_url, data = data)
                print(r.text)
            except requests.exceptions.RequestException as e:
                print(e)

            # check if any alerts should be triggered
            if(temp > settings['high_temp'] or temp < settings['low_temp']
                    or humidity > settings['high_humidity'] or humidity < settings['low_humidity']
                    or pressure > settings['high_pressure'] or pressure < settings['low_pressure']):
                unsafe()
            else:
                safe()

            sleep(2000)

        else:
            print('Unable to retrieve alert settings.')

if __name__ == '__main__':
    main()