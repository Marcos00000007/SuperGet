from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from app import db
from models.venda import Venda
from models.item_venda import ItemVenda
from models.produto import Produto
from models.cliente import Cliente
from datetime import datetime, date

vendas_bp = Blueprint('vendas', __name__, url_prefix='/vendas')

@vendas_bp.route('/')
@login_required
def listar():
    data_inicio = request.args.get('data_inicio', date.today().replace(day=1).isoformat())
    data_fim = request.args.get('data_fim', date.today().isoformat())
    forma_pagamento = request.args.get('forma_pagamento', '')

    query = Venda.query.filter(
        db.func.date(Venda.data_venda) >= data_inicio,
        db.func.date(Venda.data_venda) <= data_fim
    )

    if forma_pagamento:
        query = query.filter_by(forma_pagamento=forma_pagamento)

    vendas = query.order_by(Venda.data_venda.desc()).all()

    total_periodo = sum(float(v.total) for v in vendas)
    ticket_medio = total_periodo / len(vendas) if vendas else 0

    return render_template('vendas.html',
        vendas=vendas,
        data_inicio=data_inicio,
        data_fim=data_fim,
        forma_pagamento=forma_pagamento,
        total_periodo=total_periodo,
        ticket_medio=ticket_medio
    )

@vendas_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova():
    clientes = Cliente.query.order_by(Cliente.nome).all()
    produtos = Produto.query.filter(Produto.ativo==True, Produto.estoque_atual > 0).order_by(Produto.nome).all()

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id') or None
        forma_pagamento = request.form.get('forma_pagamento')
        produto_ids = request.form.getlist('produto_id[]')
        quantidades = request.form.getlist('quantidade[]')

        if not produto_ids or not forma_pagamento:
            flash('Selecione ao menos um produto e a forma de pagamento.', 'danger')
            return render_template('nova_venda.html', clientes=clientes, produtos=produtos)

        total = 0
        itens_dados = []

        for pid, qtd in zip(produto_ids, quantidades):
            produto = Produto.query.get(int(pid))
            qtd = int(qtd)

            if not produto or qtd <= 0:
                continue
            if produto.estoque_atual < qtd:
                flash(f'Estoque insuficiente para {produto.nome}.', 'danger')
                return render_template('nova_venda.html', clientes=clientes, produtos=produtos)

            subtotal = float(produto.preco_venda) * qtd
            total += subtotal
            itens_dados.append({
                'produto': produto,
                'quantidade': qtd,
                'preco_unitario': float(produto.preco_venda),
                'subtotal': subtotal
            })

        if not itens_dados:
            flash('Nenhum item válido na venda.', 'danger')
            return render_template('nova_venda.html', clientes=clientes, produtos=produtos)

        # Criar a venda
        venda = Venda(
            cliente_id=int(cliente_id) if cliente_id else None,
            usuario_id=current_user.id,
            total=total,
            forma_pagamento=forma_pagamento
        )
        db.session.add(venda)
        db.session.flush()  # Para obter o ID da venda

        for item in itens_dados:
            iv = ItemVenda(
                venda_id=venda.id,
                produto_id=item['produto'].id,
                quantidade=item['quantidade'],
                preco_unitario=item['preco_unitario'],
                subtotal=item['subtotal']
            )
            db.session.add(iv)
            # Atualizar estoque
            item['produto'].estoque_atual -= item['quantidade']

        db.session.commit()
        flash(f'Venda #{venda.id} registrada com sucesso! Total: R$ {total:.2f}', 'success')
        return redirect(url_for('vendas.listar'))

    return render_template('nova_venda.html', clientes=clientes, produtos=produtos)

@vendas_bp.route('/ver/<int:id>')
@login_required
def ver(id):
    venda = Venda.query.get_or_404(id)
    return render_template('ver_venda.html', venda=venda)

# API: buscar produto por nome (AJAX)
@vendas_bp.route('/api/produto/<int:id>')
@login_required
def api_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify({
        'id': produto.id,
        'nome': produto.nome,
        'preco_venda': float(produto.preco_venda),
        'estoque_atual': produto.estoque_atual
    })
