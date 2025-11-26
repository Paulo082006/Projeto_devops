from flask import Blueprint, request, jsonify
from models.jogos import Jogo
from db import db   
import os

jogos_bp = Blueprint('jogos', __name__)


@jogos_bp.route('/jogos', methods=["GET"])
def get_jogos():
    jogos = db.session.execute(db.select(Jogo)).scalars().all()
    jogo = [i.to_dict() for i in jogos]
    return jsonify(mensagem='Jogos obtidos com sucesso!', jogos = jogo), 200


@jogos_bp.route('/jogos', methods=["POST"])
def post_jogos():
    data = request.get_json()
    jogo = Jogo(data['nome'], data['genero'], data['classe_etaria'])
    db.session.add(jogo)
    db.session.commit()
    return jsonify(mensagem='Jogo criado com sucesso!', jogo = jogo.to_dict()), 201


@jogos_bp.route('/jogos/<int:id>', methods=["GET"])
def get_jogo(id):
    jogo = db.get_or_404(Jogo, id)
    return jsonify(mensagem='Jogo obtido com sucesso!', jogo = jogo.to_dict()), 200


@jogos_bp.route('/jogos/<int:id>', methods=["PUT"])
def update_jogo(id):    
    data = request.get_json()
    jogo = db.get_or_404(Jogo, id)
    jogo.nome = data['nome']
    jogo.genero = data['genero']
    jogo.classe_etaria = data['classe_etaria']
    db.session.commit()
    return jsonify(mensagem='Jogo atualizado com sucesso!', jogo = jogo.to_dict()), 200 


@jogos_bp.route('/jogos/<int:id>', methods=["DELETE"])
def delete_jogo(id):
    jogo = db.get_or_404(Jogo, id)
    db.session.delete(jogo)
    db.session.commit()
    return jsonify(mensagem='Jogo deletado com sucesso!'), 200

