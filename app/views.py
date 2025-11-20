# app/views.py
from flask import render_template, request, redirect, url_for, session, jsonify
from .models import db, Produto, Supermercado, Lista
import requests # Usado na rota de localização

# REMOVER ESSAS LINHAS:
# from . import create_app
# app = create_app()

def register_routes(app):
    """Função que registra todas as rotas no objeto Flask app."""

    # --- Rotas Principais e CRUD (PJI110) ---

    @app.route('/')
    def index():
        """Rota inicial: exibe painel e localização."""
        produtos = Produto.query.all()
        supermercados = Supermercado.query.all()
        listas = Lista.query.all()
        
        # Obtém a localização da sessão para exibição
        user_location_display = session.get('user_location', {}).get('region', 'Não detectada/definida')
        
        return render_template('index.html', 
                               produtos=produtos, 
                               supermercados=supermercados,
                               listas=listas,
                               user_location_display=user_location_display)

    @app.route('/produto/novo', methods=['GET', 'POST'])
    def novo_produto():
        """Cria um novo produto."""
        if request.method == 'POST':
            nome = request.form.get('nome')
            categoria = request.form.get('categoria')
            preco = request.form.get('preco')
            
            try:
                novo_p = Produto(nome=nome, categoria=categoria, preco_medio=float(preco) if preco else 0.0)
                db.session.add(novo_p)
                db.session.commit()
                return redirect(url_for('index'))
            except ValueError:
                return "Erro: Preço inválido.", 400

        return render_template('form_produto.html')

    @app.route('/supermercado/novo', methods=['GET', 'POST'])
    def novo_supermercado():
        """Cria um novo supermercado."""
        if request.method == 'POST':
            nome = request.form.get('nome')
            novo_s = Supermercado(nome=nome)
            db.session.add(novo_s)
            db.session.commit()
            return redirect(url_for('index'))
        
        return render_template('form_supermercado.html')


    # --- Rota de Localização (Implementação PJI240) ---

    @app.route('/set_location', methods=['POST'])
    def set_location():
        """Recebe dados de localização do frontend (JavaScript) e armazena na sessão."""
        data = request.get_json()
        
        region = None
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if data.get('region'):
            region = data['region']
            session['user_location'] = {'type': 'manual', 'region': region}
            message = f"Localização definida manualmente: {region}"
            current_region = region
        
        elif lat and lon:
            region = f"({lat:.2f}, {lon:.2f})"
            session['user_location'] = {'type': 'auto', 'latitude': lat, 'longitude': lon, 'region': region}
            message = f"Localização detectada: {region}"
            current_region = f"Coordenadas: {region}"
        
        else:
            return jsonify({'status': 'error', 'message': 'Dados de localização inválidos.'}), 400

        return jsonify({'status': 'success', 'message': message, 'current_region': current_region})