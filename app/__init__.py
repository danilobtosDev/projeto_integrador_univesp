# app/__init__.py
from flask import Flask
from .models import db
import os # Importar módulo os para manipulação de caminhos

def create_app():
    # Define o caminho absoluto para a pasta 'templates'
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    
    # Passa o caminho explicitamente para o Flask
    app = Flask(__name__, template_folder=template_dir)
    
    # --- Configurações do Flask ---
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'chave_de_comparacao_super_secreta'
    # -----------------------------
    
    db.init_app(app)
    
    with app.app_context():
        from .views import register_routes
        register_routes(app)
        
        db.create_all()
        
        return app