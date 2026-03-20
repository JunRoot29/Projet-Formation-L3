from app import db
from app.models import TrainingRequest, Enrollment, Session


def approve_request(request_id, training_id=None):
    req = TrainingRequest.query.get_or_404(request_id)
    if training_id is not None:
        req.training_id = training_id
    req.statut = "APPROVED"
    db.session.commit()
    return req


def reject_request(request_id):
    req = TrainingRequest.query.get_or_404(request_id)
    req.statut = "REJECTED"
    db.session.commit()
    return req


def register_employee(request_id, session_id):
    req = TrainingRequest.query.get_or_404(request_id)
    session = Session.query.get_or_404(session_id)
    if req.enrollment:
        return req.enrollment
    if req.training_id and req.training_id != session.training_id:
        raise ValueError("La session ne correspond pas a la formation selectionnee.")
    if len(session.enrollments) >= session.capacite:
        raise ValueError("La session selectionnee est complete.")
    enrollment = Enrollment(request=req, session=session, statut="REGISTERED")
    db.session.add(enrollment)
    db.session.commit()
    return enrollment


def cancel_enrollment(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    enrollment.statut = "CANCELLED"
    db.session.commit()
    return enrollment


def complete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    if enrollment.statut != "REGISTERED":
        raise ValueError("Seules les inscriptions actives peuvent etre terminees.")
    enrollment.statut = "COMPLETED"
    db.session.commit()
    return enrollment
