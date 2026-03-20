from app import db
from app.models import User, Training, Session, Invoice
from datetime import date


def seed_demo_data():
    if User.query.first():
        return

    manager = User(nom="Manager", email="manager@company.com", role="MANAGER")
    manager.set_password("password")

    employee = User(nom="Employé", email="employee@company.com", role="EMPLOYEE")
    employee.set_password("password")

    t1 = Training(titre="Python Avancé", description="Maîtriser Python", organisme="OpenEdu")
    t2 = Training(titre="Gestion de Projet", description="Méthodes Agile", organisme="AgilePro")

    s1 = Session(training=t1, date=date(2026, 4, 10), lieu="Paris", capacite=15)
    s2 = Session(training=t1, date=date(2026, 5, 5), lieu="Lyon", capacite=10)
    s3 = Session(training=t2, date=date(2026, 4, 20), lieu="Marseille", capacite=20)

    inv1 = Invoice(training=t1, montant=1500, statut="PENDING")

    db.session.add_all([manager, employee, t1, t2, s1, s2, s3, inv1])
    db.session.commit()
