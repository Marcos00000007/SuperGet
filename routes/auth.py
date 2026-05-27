from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(email=email, ativo=True).first()

        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

# Dashboard (rota raiz autenticada)
from flask import Blueprint as _BP
from flask_login import login_required as _lr
from app import db
from models.produto import Produto
from models.venda import Venda
from models.cliente import Cliente
from models.fornecedor import Fornecedor
from datetime import datetime, date
from sqlalchemy import func

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    total_produtos = Produto.query.filter_by(ativo=True).count()
    total_clientes = Cliente.query.count()
    total_fornecedores = Fornecedor.query.count()

    hoje = date.today()
    vendas_hoje = Venda.query.filter(
        func.date(Venda.data_venda) == hoje
    ).all()
    faturamento_hoje = sum(float(v.total) for v in vendas_hoje)

    estoque_baixo = Produto.query.filter(
        Produto.estoque_atual <= Produto.estoque_minimo,
        Produto.estoque_atual > 0,
        Produto.ativo == True
    ).count()

    sem_estoque = Produto.query.filter(
        Produto.estoque_atual == 0,
        Produto.ativo == True
    ).count()

    ultimas_vendas = Venda.query.order_by(Venda.data_venda.desc()).limit(5).all()

    return render_template('dashboard.html',
        total_produtos=total_produtos,
        total_clientes=total_clientes,
        total_fornecedores=total_fornecedores,
        faturamento_hoje=faturamento_hoje,
        estoque_baixo=estoque_baixo,
        sem_estoque=sem_estoque,
        ultimas_vendas=ultimas_vendas
    )

# Registrar a rota de dashboard no app principal
from flask import current_app
