#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = db.session.get(Animal, id)
    if not animal:
        return "Animal not found", 404
    return f"""
    <ul>Name: {animal.name}</ul>
    <ul>Species: {animal.species}</ul>
    <ul>Zookeeper: {animal.zookeeper.name if animal.zookeeper else 'None'}</ul>
    <ul>Enclosure: {animal.enclosure.environment if animal.enclosure else 'None'}</ul>
    """

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = db.session.get(Zookeeper, id)
    if not zookeeper:
        return "Zookeeper not found", 404
    animal_names = ', '.join([animal.name for animal in zookeeper.animals if animal and animal.name])

    return f"""
    <ul>Name: {zookeeper.name}</ul>
    <ul>Birthday: {zookeeper.birthday}</ul>
    <ul>Animals: {animal_names}</ul>
    """

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = db.session.get(Enclosure, id)
    if not enclosure:
        return "Enclosure not found", 404
    animal_names = ', '.join([animal.name for animal in enclosure.animals if animal and animal.name])
    open_str = "Yes" if enclosure.open_to_visitors else "No"
    return f"""
    <ul>Environment: {enclosure.environment}</ul>
    <ul>Open to Visitors: {open_str}</ul>
    <ul>Animals: {animal_names}</ul>
    """


