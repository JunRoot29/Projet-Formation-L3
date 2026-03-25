from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app import db
from app.forms import AdminUserForm, SessionForm, TrainingForm
from app.models import Invoice, Session, Training, TrainingRequest, User
from app.services import approve_request, cancel_enrollment, register_employee, reject_request
from app.utils.security import role_required

manager_bp = Blueprint("manager", __name__)


@manager_bp.route("/dashboard")
@login_required
@role_required("MANAGER")
def dashboard():
    requests = TrainingRequest.query.all()
    invoices = Invoice.query.all()
    trainings = Training.query.all()
    sessions = Session.query.all()
    users = User.query.order_by(User.role.desc(), User.nom.asc()).all()
    user_form = AdminUserForm()
    stats = {
        "pending": TrainingRequest.query.filter_by(statut="PENDING").count(),
        "approved": TrainingRequest.query.filter_by(statut="APPROVED").count(),
        "rejected": TrainingRequest.query.filter_by(statut="REJECTED").count(),
    }
    return render_template(
        "dashboard_manager.html",
        requests=requests,
        invoices=invoices,
        stats=stats,
        trainings=trainings,
        sessions=sessions,
        users=users,
        user_form=user_form,
    )


@manager_bp.route("/users", methods=["POST"])
@login_required
@role_required("MANAGER")
def create_or_recreate_user():
    form = AdminUserForm()
    if not form.validate_on_submit():
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, "danger")
        return redirect(url_for("manager.dashboard"))

    email = form.email.data.strip().lower()
    user = User.query.filter_by(email=email).first()
    created = user is None

    if created:
        user = User(email=email)
        db.session.add(user)

    user.nom = form.nom.data.strip()
    user.role = form.role.data
    user.set_password(form.password.data)
    db.session.commit()

    flash("Compte cree." if created else "Compte recree et mot de passe reinitialise.", "success")
    return redirect(url_for("manager.dashboard"))


@manager_bp.route("/requests/<int:request_id>/approve", methods=["POST"])
@login_required
@role_required("MANAGER")
def approve(request_id):
    training_id = None
    if "training_id" in request.form and request.form.get("training_id"):
        training_id = int(request.form.get("training_id"))
    approve_request(request_id, training_id=training_id)
    flash("Demande approuvee", "success")
    return redirect(url_for("manager.dashboard"))


@manager_bp.route("/requests/<int:request_id>/reject", methods=["POST"])
@login_required
@role_required("MANAGER")
def reject(request_id):
    reject_request(request_id)
    flash("Demande rejetee", "danger")
    return redirect(url_for("manager.dashboard"))


@manager_bp.route("/catalogue", methods=["GET", "POST"])
@login_required
@role_required("MANAGER")
def catalogue_manager():
    trainings = Training.query.all()
    form = TrainingForm()
    if form.validate_on_submit():
        training = Training(titre=form.titre.data, description=form.description.data, organisme=form.organisme.data)
        db.session.add(training)
        db.session.commit()
        flash("Formation ajoutee", "success")
        return redirect(url_for("manager.catalogue_manager"))
    return render_template("catalogue_manager.html", trainings=trainings, form=form)


@manager_bp.route("/sessions/<int:training_id>", methods=["GET", "POST"])
@login_required
@role_required("MANAGER")
def sessions(training_id):
    training = Training.query.get_or_404(training_id)
    form = SessionForm()
    if form.validate_on_submit():
        session = Session(training_id=training_id, date=form.date.data, lieu=form.lieu.data, capacite=form.capacite.data)
        db.session.add(session)
        db.session.commit()
        flash("Session ajoutee", "success")
        return redirect(url_for("manager.sessions", training_id=training_id))
    return render_template("sessions_manager.html", training=training, form=form)


@manager_bp.route("/inscrire/<int:request_id>", methods=["POST"])
@login_required
@role_required("MANAGER")
def inscrire(request_id):
    session_id = request.form.get("session_id")
    if not session_id:
        flash("Choisissez une session avant d'inscrire l'employe.", "warning")
        return redirect(url_for("manager.dashboard"))
    try:
        register_employee(request_id, int(session_id))
        flash("Employe inscrit", "success")
    except ValueError as exc:
        flash(str(exc), "danger")
    return redirect(url_for("manager.dashboard"))


@manager_bp.route("/annuler/<int:enrollment_id>", methods=["POST"])
@login_required
@role_required("MANAGER")
def annuler(enrollment_id):
    cancel_enrollment(enrollment_id)
    flash("Inscription annulee", "warning")
    return redirect(url_for("manager.dashboard"))


@manager_bp.route("/invoices/<int:invoice_id>/verify", methods=["POST"])
@login_required
@role_required("MANAGER")
def verify_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.statut = "VERIFIED"
    db.session.commit()
    flash("Facture verifiee", "success")
    return redirect(url_for("manager.dashboard"))
