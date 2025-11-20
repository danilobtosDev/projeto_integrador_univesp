# app/__init__.py
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    
    # --- Configurações do Flask ---
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'chave_de_comparacao_super_secreta'
    # -----------------------------
    
    db.init_app(app)
    
    with app.app_context():
        # IMPORTANTE: Agora importamos e CHAMAMOS a função de registro
        from .views import register_routes
        register_routes(app)
        
        db.create_all()  # Cria as tabelas
        
        return app