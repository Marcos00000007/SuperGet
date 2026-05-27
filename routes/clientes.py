from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from models.cliente import Cliente
from utils.validators import limpar_cpf, validar_cpf

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/')
@login_required
def listar():
    busca = request.args.get('busca', '')
    query = Cliente.query
    if busca:
        query = query.filter(Cliente.nome.ilike(f'%{busca}%'))
    clientes = query.order_by(Cliente.nome).all()
    return render_template('clientes.html', clientes=clientes, busca=busca)

@clientes_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf_raw = request.form.get('cpf', '').strip()
        cpf = limpar_cpf(cpf_raw) if cpf_raw else None
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()

        if not nome:
            flash('Informe o nome do cliente.', 'danger')
            return render_template('cliente_form.html', cliente=None)

        if cpf and not validar_cpf(cpf):
            flash('CPF inválido.', 'danger')
            return render_template('cliente_form.html', cliente=None)

        if cpf and Cliente.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado.', 'warning')
            return render_template('cliente_form.html', cliente=None)

        cliente = Cliente(nome=nome, cpf=cpf, telefone=telefone, email=email)
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado!', 'success')
        return redirect(url_for('clientes.listar'))

    return render_template('cliente_form.html', cliente=None)

@clientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nome = request.form.get('nome', '').strip()
        cliente.telefone = request.form.get('telefone', '').strip()
        cliente.email = request.form.get('email', '').strip()
        db.session.commit()
        flash('Cliente atualizado!', 'success')
        return redirect(url_for('clientes.listar'))

    return render_template('cliente_form.html', cliente=cliente)

@clientes_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente removido.', 'success')
    return redirect(url_for('clientes.listar'))
