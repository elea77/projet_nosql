from flask import Blueprint, render_template

concert = Blueprint("concert", __name__, static_folder="static", template_folder="templates")

@concert.route("/concerts")
def concerts():
    return "Page des concerts !"