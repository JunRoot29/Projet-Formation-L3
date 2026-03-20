from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="EMPLOYEE")

    training_requests = db.relationship("TrainingRequest", back_populates="employee", cascade="all, delete-orphan")
    feedbacks = db.relationship("Feedback", back_populates="employee", cascade="all, delete-orphan")

    def set_password(self, password):
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
