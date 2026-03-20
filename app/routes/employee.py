from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Training, TrainingRequest, Session, Enrollment, Feedback
from app.forms import TrainingRequestForm, SessionChoiceForm, FeedbackForm
from app.services import cancel_enrollment, complete_enrollment
from app.utils.security import role_required
from app.utils.files import save_uploaded_file

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/dashboard")
@login_required
@role_required("EMPLOYEE")
def dashboard():
    requests = TrainingRequest.query.filter_by(employee_id=current_user.id).all()
    enrollments = Enrollment.query.join(TrainingRequest).filter(TrainingRequest.employee_id == current_user.id).all()
    return render_template("dashboard.html", requests=requests, enrollments=enrollments)


@employee_bp.route("/catalogue")
@login_required
@role_required("EMPLOYEE")
def catalogue():
    trainings = Training.query.all()
    return render_template("catalogue.html", trainings=trainings)


@employee_bp.route("/demande/<int:training_id>", methods=["GET", "POST"])
@login_required
@role_required("EMPLOYEE")
def demande(training_id):
    training = Training.query.get_or_404(training_id)
    form = TrainingRequestForm()
    if form.validate_on_submit():
        req = TrainingRequest(employee_id=current_user.id, training_id=training_id, statut="PENDING")
        db.session.add(req)
        db.session.commit()
        flash("Demande soumise", "success")
        return redirect(url_for("employee.dashboard"))
    return render_template("demande.html", training=training, form=form)


@employee_bp.route("/suivi")
@login_required
@role_required("EMPLOYEE")
def suivi():
    requests = TrainingRequest.query.filter_by(employee_id=current_user.id).all()
    return render_template("suivi.html", requests=requests)


@employee_bp.route("/choisir-session/<int:request_id>", methods=["GET", "POST"])
@login_required
@role_required("EMPLOYEE")
def choisir_session(request_id):
    req = TrainingRequest.query.get_or_404(request_id)
    if req.employee_id != current_user.id:
        flash("Cette demande ne vous appartient pas.", "danger")
        return redirect(url_for("employee.dashboard"))

    if req.training_id:
        sessions = Session.query.filter_by(training_id=req.training_id).all()
    else:
        sessions = Session.query.all()

    if not sessions:
        flash("Aucune session disponible pour le moment.", "warning")
        return redirect(url_for("employee.dashboard"))

    form = SessionChoiceForm()
    form.session_id.choices = [(s.id, f"{s.training.titre} - {s.date} - {s.lieu}") for s in sessions]

    if form.validate_on_submit():
        if req.enrollment:
            flash("Une session est deja associee a cette demande.", "warning")
            return redirect(url_for("employee.dashboard"))

        session = Session.query.get_or_404(form.session_id.data)
        if len(session.enrollments) >= session.capacite:
            flash("Cette session est complete.", "danger")
            return redirect(url_for("employee.choisir_session", request_id=req.id))

        enrollment = Enrollment(request=req, session_id=form.session_id.data, statut="REGISTERED")
        db.session.add(enrollment)
        db.session.commit()
        flash("Session choisie", "success")
        return redirect(url_for("employee.dashboard"))

    return render_template("demande.html", training=None, form=form, choose_session=True, request_item=req)


@employee_bp.route("/annuler/<int:enrollment_id>", methods=["POST"])
@login_required
@role_required("EMPLOYEE")
def annuler(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    if enrollment.request.employee_id != current_user.id:
        flash("Cette inscription ne vous appartient pas.", "danger")
        return redirect(url_for("employee.dashboard"))
    cancel_enrollment(enrollment_id)
    flash("Annulation demandee", "warning")
    return redirect(url_for("employee.dashboard"))


@employee_bp.route("/feedback/<int:training_id>", methods=["GET", "POST"])
@login_required
@role_required("EMPLOYEE")
def feedback(training_id):
    training = Training.query.get_or_404(training_id)
    form = FeedbackForm()
    if form.validate_on_submit():
        filename = save_uploaded_file(form.fichier.data) if form.fichier.data else None
        fb = Feedback(employee_id=current_user.id, training_id=training_id, commentaire=form.commentaire.data, fichier=filename)
        db.session.add(fb)
        db.session.commit()
        flash("Feedback envoye", "success")
        return redirect(url_for("employee.dashboard"))
    return render_template("feedback.html", form=form, training=training)


@employee_bp.route("/completion/<int:enrollment_id>", methods=["POST"])
@login_required
@role_required("EMPLOYEE")
def completion(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    if enrollment.request.employee_id != current_user.id:
        flash("Cette inscription ne vous appartient pas.", "danger")
        return redirect(url_for("employee.dashboard"))
    try:
        complete_enrollment(enrollment_id)
        flash("Formation terminee", "success")
    except ValueError as exc:
        flash(str(exc), "warning")
    return redirect(url_for("employee.dashboard"))
