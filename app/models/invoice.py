from app import db

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    statut = db.Column(db.String(20), nullable=False, default="PENDING")

    training = db.relationship("Training", back_populates="invoices")
