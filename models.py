from app import db
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))