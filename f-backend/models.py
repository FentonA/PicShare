import os
from flask_sqlalchemy import SQLAlchemy
import sqlite3

db = SQLAlchemy()

def db_init(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()


class Pic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __init__(self, img, name, mimetype):
        self.img = img
        self.name = name
        self.mimetype = mimetype

