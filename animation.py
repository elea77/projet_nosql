from flask import Blueprint, render_template
import db

animation = Blueprint("animation", __name__, static_folder="static", template_folder="templates")

@animation.route("/animations")
def animations():

    animations = db.db.api.find({"fields.category": { "$regex": '^Animations' }}, {"fields.title":1, "fields.category": 1, "fields.date_end": 1, "fields.cover_url":1, "recordid":1 }).sort([("fields.date_end", -1)]).limit(8)
    
    return render_template('animations.html', animations=animations)

