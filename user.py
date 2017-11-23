from flask_login import UserMixin
from app import db


class User(db.Model):
    __tablename__ = "USERD"
    userid = db.Column(db.string, primary_key= True)
    password = db.Column(db.string)
    type = db.Column(db.string)
