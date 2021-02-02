from flask import Blueprint, render_template

animation = Blueprint("animation", __name__, static_folder="static", template_folder="templates")

# exemple d'insertion
@animation.route("/animations")
def animations():
    return "Page des animations !"
