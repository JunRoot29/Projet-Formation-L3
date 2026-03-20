from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired

class TrainingRequestForm(FlaskForm):
    submit = SubmitField("Soumettre la demande")

class SessionChoiceForm(FlaskForm):
    session_id = SelectField("Session", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Choisir la session")

class EnrollmentCancelForm(FlaskForm):
    submit = SubmitField("Demander annulation")

class FeedbackForm(FlaskForm):
    commentaire = TextAreaField("Commentaire", validators=[DataRequired()])
    fichier = FileField("Attestation de présence")
    submit = SubmitField("Envoyer")
