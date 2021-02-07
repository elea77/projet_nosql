from flask import Blueprint, render_template
import db

concert = Blueprint("concert", __name__, static_folder="static", template_folder="templates")

@concert.route("/concerts")
def concerts():
    
    concerts = db.db.api.find({"fields.category": { "$regex": '^Concerts' }}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1, "recordid":1 }).sort([("fields.date_end", -1)]).limit(8)
    
    return render_template('concerts.html', concerts=concerts)

