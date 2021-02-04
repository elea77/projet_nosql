from flask import Flask, render_template, json
from flask_bootstrap import Bootstrap
from flask_pymongo import pymongo
import requests, db
from animation import animation
from concert import concert
from exposition import exposition

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.register_blueprint(animation, url_prefix="")
app.register_blueprint(concert, url_prefix="")
app.register_blueprint(exposition, url_prefix="")


# Importer les données de l'api dans la base de données
with open('data-api.json') as file: 
    file_data = json.load(file) 
      
@app.route("/api-doc")
def api_doc():
    db.client.drop_database("nosql_db")
    db.db.api.insert_many(file_data)
    return "Eléments ajoutés en bdd !"
 
@app.route("/api")
def api():
    db.client.drop_database("nosql_db")
    api = requests.get("https://opendata.paris.fr/api/records/1.0/search/?dataset=que-faire-a-paris-&q=&rows=2000")
    json_obj = api.json()
    data_api = list(json_obj["records"])

    db.db.api.insert_many(data_api)
    return "Eléments ajoutés en bdd !"
 

@app.route('/')
def index():
    titre = "Page d'accueil"
    return render_template('index.html', titre=titre)
    
    
# L’application démarre à partir de cette ligne.
if __name__=='__main__':
    app.secret_key = '6590c29cf14027ffe0cf70d4c826f104'
    app.run(debug=True)