from flask import Blueprint, render_template

concert = Blueprint("concert", __name__, static_folder="static", template_folder="templates")

# exemple d'insertion
@concert.route("/concert")
def concert():
    return "Page des concerts !"