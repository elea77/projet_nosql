from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_pymongo import pymongo
import requests, db

app = Flask(__name__)
bootstrap = Bootstrap(app)


# exemple d'insertion
@app.route("/test")
def test():
    db.db.test.insert_one({"name": "test"})
    return "Connected to the database!"


@app.route('/')
def index():
    titre = "Page d'accueil"
    return render_template('index.html', titre=titre)
    
    
# L’application démarre à partir de cette ligne.
if __name__=='__main__':
    app.secret_key = '6590c29cf14027ffe0cf70d4c826f104'
    app.run(debug=True)