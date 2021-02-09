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
    
    free_event = db.db.api.find({'fields.price_type': "gratuit"}, {"fields.title":1, "fields.address_street": 1, "fields.cover_url":1, "fields.id":1 }).limit(8)

    pmr_event = db.db.api.find({'fields.pmr': 1}, {"fields.title":1, "fields.address_street": 1, "fields.cover_url":1, "fields.id":1 }).limit(8)
    
    reservation_event = db.db.api.find({'fields.access_type': "reservation"}, {"fields.title":1, "fields.address_street": 1, "fields.cover_url":1, "fields.id":1 }).limit(8)

    return render_template('index.html', free_event=free_event, pmr_event=pmr_event, reservation_event=reservation_event)


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

    # Get data for category "A la une"
    data = db.db.api.find({"fields.category": { "$regex": re.compile(category, re.IGNORECASE)}}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1, "fields.id":1 }).sort([("fields.date_end", -1)]).limit(8)
    
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
    data = db.db.api.find({"fields.category": { "$regex": re.compile(subcategory, re.IGNORECASE)}}, {"fields.title":1, "fields.category": 1, "fields.cover_url":1, "fields.id":1 })
    
    return render_template('subcategory.html', data=data, category=category, subcategory=subcategory)



@app.route("/event/<id>")
def event(id):

    event = db.db.api.find_one({"fields.id": id}, {"fields.title":1, "fields.category": 1, "fields.date_description": 1, "fields.cover_url":1, "fields.id":1, "fields.description":1, "fields.price_detail":1,"fields.lead_text":1, "fields.address_street": 1, "fields.price_type":1, "fields.transport":1, "fields.access_link":1, "fields.address_name":1, "fields.contact_mail":1})
    
    field_description = event['fields']['description']
    field_date_description = event['fields']['date_description']

    date_description = field_date_description.split('<br />')

    clean = re.compile('<.*?>')
    description = re.sub(clean, ' ', field_description)
    description = re.sub('&amp;', '', description)

    return render_template('event.html', event=event, description=description, date_description=date_description)

    
# L’application démarre à partir de cette ligne.
if __name__=='__main__':
    app.secret_key = '6590c29cf14027ffe0cf70d4c826f104'
    app.run(debug=True)