from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from models.categoria import Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/')
@login_required
def listar():
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template('categorias.html', categorias=categorias)

@categorias_bp.route('/nova', methods=['POST'])
@login_required
def nova():
    nome = request.form.get('nome', '').strip()
    descricao = request.form.get('descricao', '').strip()

    if not nome:
        flash('Informe o nome da categoria.', 'danger')
        return redirect(url_for('categorias.listar'))

    if Categoria.query.filter_by(nome=nome).first():
        flash('Já existe uma categoria com esse nome.', 'warning')
        return redirect(url_for('categorias.listar'))

    categoria = Categoria(nome=nome, descricao=descricao)
    db.session.add(categoria)
    db.session.commit()
    flash('Categoria cadastrada!', 'success')
    return redirect(url_for('categorias.listar'))

@categorias_bp.route('/editar/<int:id>', methods=['POST'])
@login_required
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    categoria.nome = request.form.get('nome', '').strip()
    categoria.descricao = request.form.get('descricao', '').strip()
    db.session.commit()
    flash('Categoria atualizada!', 'success')
    return redirect(url_for('categorias.listar'))

@categorias_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    categoria = Categoria.query.get_or_404(id)
    if categoria.produtos:
        flash('Não é possível excluir: categoria possui produtos vinculados.', 'danger')
        return redirect(url_for('categorias.listar'))
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria removida.', 'success')
    return redirect(url_for('categorias.listar'))
