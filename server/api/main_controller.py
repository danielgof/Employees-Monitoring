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
cache = redis.Redis(host='127.0.0.1', port=6379)
if not os.path.isdir("./log"):
    os.mkdir("./log")
logging.basicConfig(filename=f'./log/{date.today()}.log', level=logging.DEBUG)
main_controller = Blueprint('main', __name__)
"""
main api
"""
@main_controller.route("/api/v1/num_visits", methods=["GET"])
def num_visits():
    count = get_hit_counts()
    current_app.logger.info(f"Number of visitors of portal at {datetime.today().strftime('%Y-%m-%d')} is {count}")
    return jsonify({"visited": count})


@main_controller.route("/api/v1/get_all_people_data", methods=["GET"])
def get_all_data():    
    try:
        data = session.query(Person).all()
        res = list()
        for person in data:
            all_phones = []
            phone_num = session.query(Phone) \
            .join(Phone, Person.phones) \
            .filter(Person.id == person.id) \
            .all()
            # print(phone_num)
            for phone in phone_num:
                all_phones.append(phone.phone)
            # all_phones = map(lambda x: x.phone, phone_num)
            # # all_phones.extend(phone_num)
            # print(all_phones)
            position = session.query(Positon).filter(Positon.id == person.position_id).first()
            if position == None:
                continue
            if phone_num == None:
                continue
            res.append({
            "id": person.id,
            "position": position.position,
            "last_name": person.last_name,
            "first_name": person.first_name,
            "salary": position.salary,
            "department": position.departament,
            "phone": all_phones
            })
        current_app.logger.info("All users were selected from database")
        return res 
    except Exception as e:
        current_app.logger.warning(f"Exeption {e} ocured")
        abort(Response(e, 500))


@main_controller.route("/api/v1/get_all_positions", methods=["GET"])
def positions_info():
    try:
        data = session.query(Positon).all()
        res = list()
        for position in data:
            res.append({
            "id":position.id,
            "position": position.position,
            "salary": position.salary,
            "department": position.departament
            })
        current_app.logger.info("All users were selected from database")
        return res 
    except Exception as e:
        current_app.logger.warning(f"Exeption {e} ocured")
        abort(Response(e, 500))