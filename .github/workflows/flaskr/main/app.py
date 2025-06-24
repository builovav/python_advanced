import datetime
import random
import sqlite3
from typing import List

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

db = SQLAlchemy()

app_prod: dict = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///prod_db",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}
app_test: dict = {
    "SQLALCHEMY_DATABASE_URI": "sqlite://",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "TESTING": True,
}



def create_app(test_config=app_test):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(test_config)
    db.init_app(app)

    from flaskr.main.models import Clientparking, Clients, Parkings

    # @app.before_first_request
    # def before_request_func():
    #     db.create_all()

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/")
    def hello():
        return "Hello, World!"

    @app.route("/test_route")
    def math_route():
        """Тестовый роут для расчета степени"""
        number = int(request.args.get("number", 0))
        result = number**2
        return jsonify(result)

    @app.route("/clients", methods=["GET"])
    def get_clients_handler():
        """Получение списка клиентов"""
        clients: List[Clients] = db.session.query(Clients).all()
        clients_list = [u.to_json() for u in clients]
        return jsonify(clients_list), 200

    @app.route("/parkings", methods=["GET"])
    def get_parkings_handler():
        """Получение списка парковок"""
        parkings: List[Parkings] = db.session.query(Parkings).all()
        parkings_list = [u.to_json() for u in parkings]
        return jsonify(parkings_list), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_handler(client_id: int):
        """Получение клиента по ид"""
        client: Clients = db.session.query(Clients).get(client_id)  # type: ignore
        return jsonify(client.to_json()), 200

    @app.route("/clients", methods=["POST"])
    def create_client_handler():
        """Создание нового клиента"""
        name = request.form.get("name", type=str)
        surname = request.form.get("surname", type=str)
        car_number = request.form.get("car_number", type=str)
        credit_card = request.form.get("credit_card", type=str)
        new_client = Clients(
            name=name, surname=surname, credit_card=credit_card, car_number=car_number
        )
        db.session.add(new_client)
        db.session.commit()

        return "", 201

    @app.route("/parkings", methods=["POST"])
    def create_parkings_handler():
        """Создание новой парковочной зоны"""
        count_places = random.randint(1, 100)
        count_available_place = random.randint(0, count_places)
        if count_available_place > 0:
            opened = True
        else:
            opened = False
        address = request.form.get("address", type=str)
        new_parking = Parkings(
            address=address,
            count_places=count_places,
            count_available_places=count_available_place,
            opened=opened,
        )
        db.session.add(new_parking)
        db.session.commit()
        return "", 201

    @app.route("/client_parkings", methods=["POST"])
    def create_client_parkings_handler():
        """Заезд на парковку"""
        time = datetime.datetime.now()
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)
        # client_parking_data = request.json
        try:
            new_client_parking = Clientparking(
                client_id=client_id, parking_id=parking_id, time_in=time
            )
            opened_id = db.session.execute(
                select(Parkings.opened).where(Parkings.id == parking_id)
            ).scalar()
            if opened_id is True:
                if (
                    db.session.execute(
                        select(Parkings.count_available_places).where(
                            Parkings.id == parking_id
                        )
                    ).scalar()
                    > 0
                ):
                    db.session.query(Parkings).filter(Parkings.id == parking_id).update(
                        {"count_available_places": Parkings.count_available_places - 1}
                    )
                    if (
                        db.session.execute(
                            select(Parkings.count_available_places).where(
                                Parkings.id == parking_id
                            )
                        ).scalar()
                        == 0
                    ):
                        db.session.query(Parkings).filter(
                            Parkings.id == parking_id
                        ).update({"opened": Parkings.opened - 1})
                else:
                    (
                        db.session.query(Parkings)
                        .filter(Parkings.id == parking_id)
                        .update({"opened": Parkings.opened - 1})
                    )
                    db.session.commit()
                    return "Свободных мест нет", 201

                db.session.add(new_client_parking)
                db.session.commit()
                return f"Въезд на парковку в {time}", 201
            else:
                return "Парковка закрыта", 201
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed" in str(error):
                print(f"Ошибка: {error}")
            else:
                print(f"Ошибка: {error}")
        except Exception as error:
            print(f"Данные перезаписаны: {error}")
            db.session.rollback()
            opened_id = db.session.execute(
                select(Parkings.opened).where(Parkings.id == parking_id)
            ).scalar()
            time_out = db.session.execute(
                select(Clientparking.time_out).where(
                    Clientparking.parking_id == parking_id,
                    Clientparking.client_id == client_id,
                )
            ).scalar()
            if time_out:
                if opened_id is True:
                    if (
                        db.session.execute(
                            select(Parkings.count_available_places).where(
                                Parkings.id == parking_id
                            )
                        ).scalar()
                        > 0
                    ):
                        db.session.query(Parkings).filter(
                            Parkings.id == parking_id
                        ).update(
                            {
                                "count_available_places": Parkings.count_available_places
                                - 1
                            }
                        )
                        if (
                            db.session.execute(
                                select(Parkings.count_available_places).where(
                                    Parkings.id == parking_id
                                )
                            ).scalar()
                            == 0
                        ):
                            db.session.query(Parkings).filter(
                                Parkings.id == parking_id
                            ).update({"opened": Parkings.opened - 1})
                        else:
                            db.session.query(Parkings).filter(
                                Parkings.id == parking_id
                            ).update({"opened": Parkings.opened - 1})
                        db.session.commit()
                        return "Свободных мест нет", 201
                    db.session.query(Clientparking).where(
                        Clientparking.parking_id == parking_id,
                        Clientparking.client_id == client_id,
                    ).update({"time_in": time, "time_out": None})
                    db.session.commit()
                return f"Въезд на парковку в {time}", 201
            else:
                return "Ваша машина уже на парковке"

    @app.route("/client_parkings", methods=["DELETE"])
    def delete_client_parkings_handler():
        """Выезд с парковки"""
        time = datetime.datetime.now()
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)
        credit_card = db.session.execute(
            select(Clients.credit_card).where(Clients.id == client_id)
        ).scalar()
        if credit_card:
            (
                db.session.query(Parkings)
                .filter(Parkings.id == parking_id)
                .update({"count_available_places": Parkings.count_available_places + 1})
            )
            db.session.query(Clientparking).where(
                Clientparking.parking_id == parking_id,
                Clientparking.client_id == client_id,
            ).update({"time_out": time})
            opened_id = db.session.execute(
                select(Parkings.opened).where(Parkings.id == parking_id)
            ).scalar()
            if opened_id is False:
                (
                    db.session.query(Parkings)
                    .filter(Parkings.id == parking_id)
                    .update({"opened": Parkings.opened + 1})
                )
            db.session.commit()
            return "Счастливого пути!", 201
        else:
            return "Вы не оплатили парковку!", 201

    return app
