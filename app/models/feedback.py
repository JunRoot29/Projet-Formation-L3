from app import db

class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"), nullable=False)
    commentaire = db.Column(db.Text, nullable=False)
    fichier = db.Column(db.String(255), nullable=True)

    employee = db.relationship("User", back_populates="feedbacks")
    training = db.relationship("Training", back_populates="feedbacks")
