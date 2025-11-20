# app/views.py
from flask import render_template, request, redirect, url_for
from .models import db, Produto, Supermercado, Lista
from . import create_app

# Criar o objeto app
app = create_app()

@app.route('/')
def index():
    """Rota inicial que exibe as listas de cadastros."""
    produtos = Produto.query.all()
    supermercados = Supermercado.query.all()
    listas = Lista.query.all()
    return render_template('index.html', 
                           produtos=produtos, 
                           supermercados=supermercados,
                           listas=listas)

@app.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    """Cria um novo produto (C do CRUD)."""
    if request.method == 'POST':
        nome = request.form.get('nome')
        categoria = request.form.get('categoria')
        preco = request.form.get('preco')
        
        try:
            novo_p = Produto(nome=nome, categoria=categoria, preco_medio=float(preco))
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