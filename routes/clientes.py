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


@clientes_bp.route('/clientes', methods=["POST"])
def post_clientes():
    data = request.get_json()
    cliente = Cliente(data['nome'], data['telefone'], data['endereco'])
    db.session.add(cliente)
    db.session.commit()
    return jsonify(mensagem='Cliente criado com sucesso!', cliente = cliente.to_dict()), 201


@clientes_bp.route('/clientes/<int:id>', methods=["GET"])
def get_cliente(id):
    cliente = db.get_or_404(Cliente, id)
    return jsonify(mensagem='Cliente obtido com sucesso!', cliente = cliente.to_dict()), 200


@clientes_bp.route('/clientes/<int:id>', methods=["DELETE"])
def delete_cliente(id):
    cliente = db.get_or_404(Cliente, id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify(mensagem='Cliente deletado com sucesso!'), 200


@clientes_bp.route('/clientes/<int:id>', methods=["PUT"])
def update_cliente(id):
    data = request.get_json()
    cliente = db.get_or_404(Cliente, id)
    cliente.nome = data['nome']
    cliente.telefone = data['telefone']
    cliente.endereco = data['endereco']
    db.session.commit()
    return jsonify(mensagem='Cliente atualizado com sucesso!', cliente = cliente.to_dict()), 200