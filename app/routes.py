from datetime import datetime
from typing import Any, Tuple

from flask import Blueprint, jsonify, request

from .models import Client, ClientParking, Parking, db

bp = Blueprint("api", __name__)


@bp.route("/clients", methods=["GET"])
def get_clients() -> Tuple[Any, int]:
    clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in clients]), 200


@bp.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id: int) -> Tuple[Any, int]:
    client = Client.query.get_or_404(client_id)
    return (
        jsonify({"id": client.id, "name": client.name, "surname": client.surname}),
        200,
    )


@bp.route("/clients", methods=["POST"])
def create_client() -> Tuple[Any, int]:
    data: Any = request.json
    new_client = Client(**data)
    db.session.add(new_client)
    db.session.commit()
    return jsonify({"id": new_client.id}), 201


@bp.route("/parkings", methods=["POST"])
def create_parking() -> Tuple[Any, int]:
    data: Any = request.json
    new_parking = Parking(**data)
    db.session.add(new_parking)
    db.session.commit()
    return jsonify({"id": new_parking.id}), 201


@bp.route("/client_parkings", methods=["POST"])
def enter_parking() -> Tuple[Any, int]:
    data: Any = request.json
    parking = db.session.get(Parking, data["parking_id"])

    # Проверка на None для mypy, так как get может ничего не вернуть
    if parking is None:
        return jsonify({"error": "Parking not found"}), 404

    if not parking.opened or parking.count_available_places <= 0:
        return jsonify({"error": "No places or closed"}), 400

    log = ClientParking(
        client_id=data["client_id"],
        parking_id=data["parking_id"],
        time_in=datetime.now(),
    )
    parking.count_available_places -= 1
    db.session.add(log)
    db.session.commit()
    return jsonify({"id": log.id}), 201


@bp.route("/client_parkings", methods=["DELETE"])
def exit_parking() -> Tuple[Any, int]:
    data: Any = request.json
    log = ClientParking.query.filter_by(
        client_id=data["client_id"], parking_id=data["parking_id"], time_out=None
    ).first()
    client = Client.query.get(data["client_id"])

    if client is None or not client.credit_card:
        return jsonify({"error": "No credit card or client not found"}), 400

    parking = Parking.query.get(data["parking_id"])
    if log and parking:
        log.time_out = datetime.now()
        parking.count_available_places += 1
        db.session.commit()

    return jsonify({"status": "exited"}), 200