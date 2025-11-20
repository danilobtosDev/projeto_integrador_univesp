# app/__init__.py
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    # Usando SQLite para simplicidade inicial (será migrado no PJI240)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Importa as rotas para registrá-las no app
        from . import views 
        # Cria as tabelas no banco de dados, se não existirem
        db.create_all()  
        
        return app