from db import db

class Jogo(db.Model):
    __tablename__ = "jogos"


    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    genero = db.Column(db.String(20), nullable = False)
    classe_etaria = db.Column(db.String(30), nullable = False)


    def __init__(self, nome, genero, classe_etaria):
        self.nome = nome
        self.genero = genero
        self.classe_etaria = classe_etaria
    

    def to_dict(self):
        return{
            'id': self.id,
            'nome': self.nome,
            'gênero': self.genero,
            'classe etária': self.classe_etaria
        }