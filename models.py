from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialisiere die SQLAlchemy-Datenbankinstanz
db = SQLAlchemy()

# Definition des User-Modells
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    chatlog = db.Column(db.Text, default='{}')

    def __repr__(self):
        return f'<User {self.username}>'
