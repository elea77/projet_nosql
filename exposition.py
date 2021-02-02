from flask import Blueprint, render_template

exposition = Blueprint("exposition", __name__, static_folder="static", template_folder="templates")

# exemple d'insertion
@exposition.route("/expositions")
def expositions():
    return "Page des expositions !"
