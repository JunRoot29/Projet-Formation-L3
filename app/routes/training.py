from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Training

training_bp = Blueprint("training", __name__)

@training_bp.route("/")
@login_required
def index():
    trainings = Training.query.all()
    return render_template("catalogue.html", trainings=trainings)
