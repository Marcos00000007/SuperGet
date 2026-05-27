from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from models.produto import Produto
from models.categoria import Categoria
from models.fornecedor import Fornecedor

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/')
@login_required
def listar():
    busca = request.args.get('busca', '')
    categoria_id = request.args.get('categoria_id', '')
    situacao = request.args.get('situacao', '')

    query = Produto.query.filter_by(ativo=True)

    if busca:
        query = query.filter(Produto.nome.ilike(f'%{busca}%'))
    if categoria_id:
        query = query.filter_by(categoria_id=int(categoria_id))
    if situacao == 'sem_estoque':
        query = query.filter(Produto.estoque_atual == 0)
    elif situacao == 'estoque_baixo':
        query = query.filter(Produto.estoque_atual <= Produto.estoque_minimo, Produto.estoque_atual > 0)

    produtos = query.order_by(Produto.nome).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()

    return render_template('produtos.html',
        produtos=produtos,
        categorias=categorias,
        busca=busca,
        categoria_id=categoria_id,
        situacao=situacao
    )

@produtos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    categorias = Categoria.query.order_by(Categoria.nome).all()
    fornecedores = Fornecedor.query.order_by(Fornecedor.razao_social).all()

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria_id = request.form.get('categoria_id')
        fornecedor_id = request.form.get('fornecedor_id')
        codigo_barras = request.form.get('codigo_barras', '').strip() or None
        preco_custo = request.form.get('preco_custo', 0) or 0
        preco_venda = request.form.get('preco_venda')
        estoque_atual = request.form.get('estoque_atual', 0)
        estoque_minimo = request.form.get('estoque_minimo', 5)

        if not nome or not categoria_id or not fornecedor_id or not preco_venda:
            flash('Preencha todos os campos obrigatórios.', 'danger')
            return render_template('cadastrar_produto.html',
                categorias=categorias, fornecedores=fornecedores)

        produto = Produto(
            nome=nome,
            categoria_id=int(categoria_id),
            fornecedor_id=int(fornecedor_id),
            codigo_barras=codigo_barras,
            preco_custo=float(preco_custo),
            preco_venda=float(preco_venda),
            estoque_atual=int(estoque_atual),
            estoque_minimo=int(estoque_minimo)
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos.listar'))

    return render_template('cadastrar_produto.html',
        categorias=categorias, fornecedores=fornecedores, produto=None)

@produtos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    produto = Produto.query.get_or_404(id)
    categorias = Categoria.query.order_by(Categoria.nome).all()
    fornecedores = Fornecedor.query.order_by(Fornecedor.razao_social).all()

    if request.method == 'POST':
        produto.nome = request.form.get('nome', '').strip()
        produto.categoria_id = int(request.form.get('categoria_id'))
        produto.fornecedor_id = int(request.form.get('fornecedor_id'))
        produto.codigo_barras = request.form.get('codigo_barras', '').strip() or None
        produto.preco_custo = float(request.form.get('preco_custo', 0) or 0)
        produto.preco_venda = float(request.form.get('preco_venda'))
        produto.estoque_atual = int(request.form.get('estoque_atual', 0))
        produto.estoque_minimo = int(request.form.get('estoque_minimo', 5))

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos.listar'))

    return render_template('cadastrar_produto.html',
        categorias=categorias, fornecedores=fornecedores, produto=produto)

@produtos_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    produto = Produto.query.get_or_404(id)
    produto.ativo = False  # Exclusão lógica
    db.session.commit()
    flash('Produto removido.', 'success')
    return redirect(url_for('produtos.listar'))
