from flask import Blueprint, request, jsonify, abort, Response
from flask_cors import CORS
from datetime import date
from datetime import datetime, timedelta
from flask import current_app
import os
import logging
from models.db import *

Session = sessionmaker(bind=engine)
session = Session()
# cache = redis.Redis(host='127.0.0.1', port=6379)
if not os.path.isdir("./log"):
    os.mkdir("./log")
logging.basicConfig(filename=f'./log/{date.today()}.log', level=logging.DEBUG)
person_controller = Blueprint('person', __name__)

@person_controller.route("/api/v1/add_person", methods=["POST"])
def add_person():
    data = request.get_json(force=True)
    new_person = Person(
        data["lastname"],
        data["firstname"],
        data["position_id"]
    )
    new_phone = Phone(
        data["phonenumber"]
    )
    new_person.phones = [new_phone]
    session.add(new_person)
    session.add(new_phone)
    session.commit()
    session.close()
    return jsonify({"result": "succes"})


@person_controller.route("/api/v1/delete_person", methods=["DELETE"])
def delete_person():
    data = request.get_json(force=True)
    session.query(Person).filter(Person.id == data["id"]).delete()
    session.commit()
    return jsonify({"result":"success"})


@person_controller.route("/api/v1/upd_firstname", methods=["PUT"])
def upd_firstname(): 
    data = request.get_json(force=True)
    session.query(Person)\
    .filter(Person.id == data["id"])\
    .update({Person.first_name: data["firstname_new"]}, synchronize_session = False)
    session.commit()
    return jsonify({"result":"success"})


@person_controller.route("/api/v1/upd_lastname", methods=["PUT"])
def upd_lastname():
    data = request.get_json(force=True)
    session.query(Person)\
    .filter(Person.id == data["id"])\
    .update({Person.last_name: data["lastname_new"]}, synchronize_session = False)
    session.commit()
    return jsonify({"result":"success"})