from app import db

class Training(db.Model):
    __tablename__ = "trainings"

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organisme = db.Column(db.String(200), nullable=False)

    sessions = db.relationship("Session", back_populates="training", cascade="all, delete-orphan")
    feedbacks = db.relationship("Feedback", back_populates="training", cascade="all, delete-orphan")
    invoices = db.relationship("Invoice", back_populates="training", cascade="all, delete-orphan")
    requests = db.relationship("TrainingRequest", back_populates="training")


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lieu = db.Column(db.String(200), nullable=False)
    capacite = db.Column(db.Integer, nullable=False)

    training = db.relationship("Training", back_populates="sessions")
    enrollments = db.relationship("Enrollment", back_populates="session", cascade="all, delete-orphan")
