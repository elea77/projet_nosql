from flask import Blueprint, render_template
import db

spectacle = Blueprint("spectacle", __name__, static_folder="static", template_folder="templates")

@spectacle.route("/spectacles")
def spectacles():

    spectacles = db.db.api.find({"fields.category": { "$regex": '^Spectacles' }}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1, "recordid":1 }).sort([("fields.date_end", -1)]).limit(8)
    
    return render_template('spectacles.html', spectacles=spectacles)

