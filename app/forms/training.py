from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class TrainingForm(FlaskForm):
    titre = StringField("Titre", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[DataRequired()])
    organisme = StringField("Organisme", validators=[DataRequired(), Length(max=200)])
    submit = SubmitField("Enregistrer")

class SessionForm(FlaskForm):
    date = DateField("Date", validators=[DataRequired()])
    lieu = StringField("Lieu", validators=[DataRequired(), Length(max=200)])
    capacite = IntegerField("Capacité", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Ajouter session")
