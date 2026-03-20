from datetime import datetime
from app import db

class TrainingRequest(db.Model):
    __tablename__ = "training_requests"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"), nullable=True)
    statut = db.Column(db.String(20), nullable=False, default="PENDING")
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship("User", back_populates="training_requests")
    training = db.relationship("Training", back_populates="requests")
    enrollment = db.relationship("Enrollment", back_populates="request", uselist=False, cascade="all, delete-orphan")


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey("training_requests.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    statut = db.Column(db.String(20), nullable=False, default="REGISTERED")

    request = db.relationship("TrainingRequest", back_populates="enrollment")
    session = db.relationship("Session", back_populates="enrollments")
