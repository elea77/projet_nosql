from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    titre = "Page d'accueil"
    return render_template('pages/index.html', titre=titre)
    
    
# L’application démarre à partir de cette ligne.
if __name__=='__main__':
    app.secret_key = '6590c29cf14027ffe0cf70d4c826f104'
    app.run(debug=True)
