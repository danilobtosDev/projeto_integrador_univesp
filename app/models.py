# app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Supermercado(db.Model):
    """Modelo para Supermercados."""
    __tablename__ = 'supermercados'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    # Adicionar colunas de localização (Lat/Lon) será útil no PJI240
    
    def __repr__(self):
        return f'<Supermercado {self.nome}>'

class Produto(db.Model):
    """Modelo para Produtos que serão comparados."""
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    preco_medio = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<Produto {self.nome}>'

class Lista(db.Model):
    """Modelo para as Listas de Compras do Usuário."""
    __tablename__ = 'listas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Lista {self.nome}>'