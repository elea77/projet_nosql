from flask import Blueprint, render_template
import db

exposition = Blueprint("exposition", __name__, static_folder="static", template_folder="templates")

@exposition.route("/expositions")
def expositions():
    
    expositions = db.db.api.find({"fields.category": { "$regex": '^Expositions' }}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1, "recordid":1 }).sort([("fields.date_end", -1)]).limit(8)
    
    return render_template('expositions.html', expositions=expositions)

