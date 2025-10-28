from db import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), nullable = False)
    telefone = db.Column(db.String(20), nullable = False)
    endereco = db.Column(db.String(100), nullable = False)


    def __init__(self, nome, telefone , endereco):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'endereço': self.endereco

        }
