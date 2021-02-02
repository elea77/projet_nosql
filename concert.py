from flask import Blueprint, render_template
import db

concert = Blueprint("concert", __name__, static_folder="static", template_folder="templates")

@concert.route("/concerts")
def concerts():
    
    concert = db.db.api.find({"fields.category": { "$regex": '^Concerts' }}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1}).limit(10)
    print(concerts)
    return render_template('concert.html', concerts=concert)

