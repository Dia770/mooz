import os
import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy
import json

database_name = 'api_code'
username = 'root'
usermdp = 'admin'
serverAndPort = 'localhost:3306'
database_path = f"mysql+pymysql://{username}:{usermdp}@{serverAndPort}/{database_name}"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


### CODES ###
class Code(db.Model):
    __tablename__ = 'codes'

    id = Column(Integer, primary_key=True)
    hashcode = Column(String(256), nullable=False)
    statut = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    telephone = Column(String(12), nullable=False)
    montant = Column(Integer, nullable=False)
    date_time = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, hashcode, statut, user_id, telephone, montant, date_time):
        self.hashcode = hashcode
        self.statut = statut
        self.user_id = user_id
        self.telephone = telephone
        self.montant = montant
        self.datetime = date_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'hashcode': self.hashcode,
            'statut': self.statut,
            'user_id': self.user_id,
            'telephone': self.telephone,
            'montant': self.montant,
            'datetime': self.date_time
        }


### USERS ###
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(21))
    name = Column(String(64))
    password = Column(String(256))

    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'password': self.password
        }

    def format_without_password(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'password': "############"
        }


### STATIONS ###
class Station(db.Model):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    station_id = Column(String(20))
    name = Column(String(128))
    gps_code = Column(String(64), nullable=True)
    error = Column(Integer, default=0)

    def __init__(self, station_id, name, gps_code, error):
        self.station_id = station_id
        self.name = name
        self.gps_code = gps_code
        self.error = error

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'station_id': self.station_id,
            'name': self.name,
            'gps_code': self.gps_code,
            'error': self.error
        }


### CONSOMMMATIONS ###
class Consume(db.Model):
    __tablename__ = 'consommations'

    id = Column(Integer, primary_key=True)
    code_used = Column(String(64))
    success = Column(String(10))
    consumed_by = Column(String(64))
    generated_by = Column(String(64))
    date_time = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, code_used, success, consumed_by, generated_by, date_time):
        self.code_used = code_used
        self.success = success
        self.consumed_by = consumed_by
        self.generated_by = generated_by
        self.date_time = date_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'code_used': self.code_used,
            'success': self.success,
            'consumed_by': self.consumed_by,
            'generated_by': self.generated_by,
            'date_time': self.date_time
        }


### CONNEXIONS ###
class Connexion(db.Model):
    __tablename__ = 'connexions'

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, default=datetime.datetime.now())
    id_user = Column(Integer)
    username = Column(String(64))

    def __init__(self, date_time, id_user, username):
        self.date_time = date_time
        self.id_user = id_user
        self.username = username

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'date_time': self.date_time,
            'id_user': self.id_user,
            'username': self.username
        }
