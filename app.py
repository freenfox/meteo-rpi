
from flask import Flask, render_template, request, redirect, send_file, request, Response
import RPi.GPIO as GPIO
import time
import requests
from db import exec_dict, connect_db
from matplotlib.figure import Figure
from io import BytesIO
from data_plotter import *

red_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red_pin,GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def index():
    with connect_db() as cur:
        query = """
        SELECT temperature, humidity, Timestamp
        FROM mesurments
        ORDER BY Timestamp DESC
        LIMIT 1;
        """
        data = exec_dict(cur, query)[0]
        #print(data)

    return render_template("index.html", timestamp = data['Timestamp'], humidity = data['humidity'], temperatur = data['temperature'])

@app.route("/plot", methods =['POST', 'GET'])
def plot():
    timeframe = request.form.get("timeframe")
    print(timeframe) # to plug into the query

    with connect_db() as cur:
        query = """
        SELECT temperature, humidity, unixepoch(Timestamp)
        FROM mesurments
        WHERE Timestamp >= datetime('now', ?)
        ORDER BY Timestamp DESC
        """
        data = exec_dict(cur, query, params=(timeframe,))
        # print(data)

        temp_list = []
        hum_list = []
        for mesurment in data:
            temp_list.append([mesurment['unixepoch(Timestamp)'], mesurment['temperature']])
            hum_list.append([mesurment['unixepoch(Timestamp)'], mesurment['humidity']])
        # print(temp_list)
        # print(hum_list)

        # Création du graphique et rendu au format PNG
        img = plot_data(temp_list, hum_list)

        # Response permet d'envoyer des données binaires
        return Response(img.getvalue(), mimetype='image/png')

@app.route("/serve_plot")

# @app.route("/ai_command", methods =['POST'])
# def led_command():
#     message = "what did the user want the state of the light to be? INPUT: "+request.form['message']

#     payload = {
#         "question": message,
#         "options": [
#             {"option": "on", "label": "A"},
#             {"option": "off", "label": "B"}
#         ]
#     }


#     if action == 'on':
#         print("turning led on")
#         GPIO.output(red_pin,GPIO.HIGH)

#     elif action == 'off':
#         print("turning led off")
#         GPIO.output(red_pin,GPIO.LOW)
        


app.run(host='0.0.0.0',use_reloader=False, port=5000, debug = True)