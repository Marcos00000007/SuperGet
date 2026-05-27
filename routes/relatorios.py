from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from flask_login import login_required
from app import db
from models.venda import Venda
from models.item_venda import ItemVenda
from utils.pdf import gerar_relatorio_vendas
from datetime import date

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@relatorios_bp.route('/')
@login_required
def index():
    data_inicio = request.args.get('data_inicio', date.today().replace(day=1).isoformat())
    data_fim = request.args.get('data_fim', date.today().isoformat())

    vendas = Venda.query.filter(
        db.func.date(Venda.data_venda) >= data_inicio,
        db.func.date(Venda.data_venda) <= data_fim
    ).order_by(Venda.data_venda.desc()).all()

    total_vendas = len(vendas)
    faturamento = sum(float(v.total) for v in vendas)
    ticket_medio = faturamento / total_vendas if total_vendas else 0
    total_itens = sum(sum(i.quantidade for i in v.itens) for v in vendas)

    return render_template('relatorio.html',
        vendas=vendas,
        data_inicio=data_inicio,
        data_fim=data_fim,
        total_vendas=total_vendas,
        faturamento=faturamento,
        ticket_medio=ticket_medio,
        total_itens=total_itens
    )

@relatorios_bp.route('/pdf')
@login_required
def gerar_pdf():
    data_inicio = request.args.get('data_inicio', date.today().replace(day=1).isoformat())
    data_fim = request.args.get('data_fim', date.today().isoformat())

    vendas = Venda.query.filter(
        db.func.date(Venda.data_venda) >= data_inicio,
        db.func.date(Venda.data_venda) <= data_fim
    ).order_by(Venda.data_venda.desc()).all()

    total_vendas = len(vendas)
    faturamento = sum(float(v.total) for v in vendas)
    ticket_medio = faturamento / total_vendas if total_vendas else 0
    total_itens = sum(sum(i.quantidade for i in v.itens) for v in vendas)

    totais = {
        'total_vendas': total_vendas,
        'faturamento': faturamento,
        'ticket_medio': ticket_medio,
        'total_itens': total_itens
    }

    buffer = gerar_relatorio_vendas(vendas, data_inicio, data_fim, totais)

    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'relatorio_vendas_{data_inicio}_{data_fim}.pdf'
    )
