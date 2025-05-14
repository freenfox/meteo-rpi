from flask import Flask, render_template, request, redirect, send_file, request, Response
import time
import requests
from db import exec_dict, connect_db
from io import BytesIO
from data_plotter import *
from datetime import datetime
import pytz


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
        print(data)

    return render_template("index.html", timestamp = data['Timestamp'], humidity = data['humidity'], temperatur = data['temperature'])


# Route pour la page d'affichage des données
@app.route('/get_data', methods=['GET'])
def get_data():
    
    # Réupération du choix de l'utilisateur
    datatype = request.args.get('datatype')
    timeframe = request.args.get('timeframe')

    with connect_db() as cur:
        query = """
        SELECT temperature, humidity, Timestamp
        FROM mesurments
        ORDER BY Timestamp DESC
        LIMIT 1;
        """
        data = exec_dict(cur, query)[0]
        #print(data)

    return render_template("index.html", timestamp = data['Timestamp'], humidity = data['humidity'], temperatur = data['temperature'], timeframe = timeframe, datatype = datatype)










@app.route('/serve_plot', methods=['GET'])
def serve_plot():
    timeframe = request.args.get("timeframe")
    print(timeframe) # to plug into the query
    datatype = request.args.get("datatype")
    print(datatype) # to plug into the query

    with connect_db() as cur:
        query = """
        SELECT temperature, humidity, unixepoch(Timestamp)
        FROM mesurments
        WHERE Timestamp >= datetime('now', ?)
        ORDER BY Timestamp DESC
        """
        data = exec_dict(cur, query, params=(timeframe,))
        # print(data)

        # format the data
        temp_list = []
        hum_list = []
        for mesurment in data:
            temp_list.append([mesurment['unixepoch(Timestamp)'], mesurment['temperature']])
            hum_list.append([mesurment['unixepoch(Timestamp)'], mesurment['humidity']])
        
        # respet the users requested datatype. juste erace the other one
        if datatype == "temperature":
            hum_list = []
        if datatype == "humidity":
            temp_list = []
        # print(temp_list)
        # print(hum_list)

        # Création du graphique et rendu au format PNG
        img = plot_data(temp_list, hum_list)

        # Response permet d'envoyer des données binaires
        return Response(img.getvalue(), mimetype='image/png')



def send_request(prompt):
    data = {
        "prompt": prompt,
        "model": "qwen2.5:0.5b",
        "stream": False,
    }
    print(data)
    response = requests.post("http://localhost:11434/api/generate", json=data)
    print(response)
    return response.json()


@app.route("/ai_slop")
def ai_slop():
    # get latest mesurement from the database
    with connect_db() as cur:
        query = """
        SELECT temperature, humidity, Timestamp
        FROM mesurments
        ORDER BY Timestamp DESC
        LIMIT 1;
        """
        current_data = exec_dict(cur, query)[0]
    
    # get a mesurment from an houre ago
    with connect_db() as cur:
        query = """
        SELECT temperature, humidity, Timestamp
        FROM mesurments
        ORDER BY datetime(Timestamp, '-1 hour') DESC
        LIMIT 1;
        """
        previous_data = exec_dict(cur, query)[0]


    cest = pytz.timezone('Europe/Berlin')
    current_time = datetime.now(cest)

    message = f'you are a parody of meteo expert. Here is the current temperature and humidity: {current_data["temperature"]}, {current_data["humidity"]}. Here is the temperature and humidity from an hour ago: {previous_data["temperature"]}, {previous_data["humidity"]}. The current time is {current_time}. Create a long and detailed analysis of this data, including predicions of the weather for the next week.'

    # send message to an local ollama instacence
    ai_awnser = send_request(message)['response']
    # print(ai_awnser)

    return ai_awnser
        

if __name__ == "__main__":
    app.run(host='0.0.0.0',use_reloader=False, port=5000, debug = True)