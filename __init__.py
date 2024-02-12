from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("Contact.html")

@app.route('/paris/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route('/commits/')
def commits():
    # Utilisation de l'API GitHub pour extraire les données sur les commits
    response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    commits_data = response.json()

    # Initialisation d'un dictionnaire pour stocker le nombre de commits par minute
    commits_per_minute = {}

    # Analyse des données pour compter le nombre de commits par minute
    for commit in commits_data:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

    # Création d'une liste de tuples (minute, nombre de commits) pour le graphique
    data_for_chart = [{'minute': minute, 'commits': commits_per_minute[minute]} for minute in commits_per_minute]

    return jsonify(data_for_chart)
  
if __name__ == "__main__":
  app.run(debug=True)
