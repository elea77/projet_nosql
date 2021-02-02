from flask import Blueprint, render_template
import db

exposition = Blueprint("exposition", __name__, static_folder="static", template_folder="templates")

@exposition.route("/expositions")
def expositions():
    
    exposition = db.db.api.find({"fields.category": { "$regex": '^Expositions' }}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1}).limit(10)
    print(expositions)
    return render_template('exposition.html', expositions=exposition)

