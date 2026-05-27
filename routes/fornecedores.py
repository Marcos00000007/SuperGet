from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from models.fornecedor import Fornecedor
from utils.validators import limpar_cnpj, validar_cnpj

fornecedores_bp = Blueprint('fornecedores', __name__, url_prefix='/fornecedores')

@fornecedores_bp.route('/')
@login_required
def listar():
    busca = request.args.get('busca', '')
    query = Fornecedor.query
    if busca:
        query = query.filter(Fornecedor.razao_social.ilike(f'%{busca}%'))
    fornecedores = query.order_by(Fornecedor.razao_social).all()
    return render_template('fornecedores.html', fornecedores=fornecedores, busca=busca)

@fornecedores_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        razao_social = request.form.get('razao_social', '').strip()
        cnpj = limpar_cnpj(request.form.get('cnpj', ''))
        telefone = request.form.get('telefone', '').strip()
        email = request.form.get('email', '').strip()

        if not razao_social or not cnpj:
            flash('Preencha os campos obrigatórios.', 'danger')
            return render_template('fornecedor_form.html', fornecedor=None)

        if not validar_cnpj(cnpj):
            flash('CNPJ inválido. Informe 14 dígitos.', 'danger')
            return render_template('fornecedor_form.html', fornecedor=None)

        if Fornecedor.query.filter_by(cnpj=cnpj).first():
            flash('CNPJ já cadastrado.', 'warning')
            return render_template('fornecedor_form.html', fornecedor=None)

        fornecedor = Fornecedor(razao_social=razao_social, cnpj=cnpj,
                                telefone=telefone, email=email)
        db.session.add(fornecedor)
        db.session.commit()
        flash('Fornecedor cadastrado!', 'success')
        return redirect(url_for('fornecedores.listar'))

    return render_template('fornecedor_form.html', fornecedor=None)

@fornecedores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    fornecedor = Fornecedor.query.get_or_404(id)

    if request.method == 'POST':
        fornecedor.razao_social = request.form.get('razao_social', '').strip()
        fornecedor.telefone = request.form.get('telefone', '').strip()
        fornecedor.email = request.form.get('email', '').strip()
        db.session.commit()
        flash('Fornecedor atualizado!', 'success')
        return redirect(url_for('fornecedores.listar'))

    return render_template('fornecedor_form.html', fornecedor=fornecedor)

@fornecedores_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    if fornecedor.produtos:
        flash('Não é possível excluir: fornecedor possui produtos vinculados.', 'danger')
        return redirect(url_for('fornecedores.listar'))
    db.session.delete(fornecedor)
    db.session.commit()
    flash('Fornecedor removido.', 'success')
    return redirect(url_for('fornecedores.listar'))
