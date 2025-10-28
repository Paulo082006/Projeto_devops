from flask import Blueprint, request, jsonify
from models.clientes import Cliente
from db import db
import os


clientes_bp = Blueprint('cliente', __name__)

@clientes_bp.route('/clientes', methods=["GET"])
def get_clientes():
    clientes = db.session.execute(db.select(Cliente)).scalars().all()
    cliente = [i.to_dict() for i in clientes]
    return jsonify(mensagem='Clientes obtidos com sucesso!', clientes = cliente), 200