from flask import Flask, render_template, json
from flask_bootstrap import Bootstrap
from flask_pymongo import pymongo
import requests, db, re

app = Flask(__name__)
bootstrap = Bootstrap(app)


# Import data from api file in db
with open('data-api.json') as file: 
    file_data = json.load(file) 
      
@app.route("/api-doc")
def api_doc():
    # Delete collection before insert
    db.client.drop_database("nosql_db")
    # Insert data in db
    db.db.api.insert_many(file_data)
    return "Eléments ajoutés en bdd !"
 
@app.route("/api")
def api():
    # Delete collection before insert
    db.client.drop_database("nosql_db")

    # Get api from url in json
    api = requests.get("https://opendata.paris.fr/api/records/1.0/search/?dataset=que-faire-a-paris-&q=&rows=2000")
    json_obj = api.json()
    data_api = list(json_obj["records"])

    # Insert data in db
    db.db.api.insert_many(data_api)

    return "Eléments ajoutés en bdd !"
 

@app.route('/')
def index():
    titre = "Page d'accueil"
    return render_template('index.html', titre=titre)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route("/category/<category>")
def category(category):

    # Get category name
    data_category = db.db.api.find_one({"fields.category": { "$regex": re.compile(category, re.IGNORECASE)} }, {"fields.category": 1 })

    field_category = data_category['fields']['category']

    # Split category for separate category and subcategory
    split_category = field_category.split(" -> ")

    category = split_category[0]

    # Get data for category
    data = db.db.api.find({"fields.category": { "$regex": re.compile(category, re.IGNORECASE)}}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1, "recordid":1 }).sort([("fields.date_end", -1)]).limit(8)
    
    return render_template('category.html', data=data, category=category)



@app.route("/subcategory/<subcategory>")
def subcategory(subcategory):

    # Get category name
    data_category = db.db.api.find_one({"fields.category": { "$regex": re.compile(subcategory, re.IGNORECASE)} }, {"fields.category": 1 })

    field_category = data_category['fields']['category']

    # Split category for separate category and subcategory
    split_category = field_category.split(" -> ")

    category = split_category[0]
    subcategory = split_category[1]
    
    # Get data for subcategory
    data = db.db.api.find({"fields.category": { "$regex": re.compile(subcategory, re.IGNORECASE)}}, {"fields.title":1, "fields.category": 1, "fields.cover_url":1, "recordid":1 })
    
    return render_template('subcategory.html', data=data, category=category, subcategory=subcategory)



@app.route("/event/<id>")
def event(id):

    event = db.db.api.find_one({"recordid": id}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1, "recordid":1, "fields.description":1, "fields.date_start":1, "fields.date_end":1, "fields.price_detail":1})
    
    # Delete HTML code in data
    field_description = event['fields']['description']
    # replace html code
    sub_description = re.sub('<p>', '', field_description)
    sub_description = re.sub('&amp; écriture', '', sub_description)
    # split description
    description = sub_description.split('</p>')


    return render_template('event.html', event=event, description=description)

    
# L’application démarre à partir de cette ligne.
if __name__=='__main__':
    app.secret_key = '6590c29cf14027ffe0cf70d4c826f104'
    app.run(debug=True)