from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from datetime import datetime

COR_VERDE = colors.HexColor('#1a7a3c')
COR_ESCURA = colors.HexColor('#1a1a2e')
COR_CINZA = colors.HexColor('#f5f5f5')

def gerar_relatorio_vendas(vendas, data_inicio, data_fim, totais):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    elementos = []

    # ----- Cabeçalho -----
    estilo_titulo = ParagraphStyle(
        'Titulo',
        parent=styles['Title'],
        fontSize=18,
        textColor=COR_VERDE,
        spaceAfter=4
    )
    estilo_sub = ParagraphStyle(
        'Sub',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey
    )

    elementos.append(Paragraph("SuperGest — Relatório de Vendas por Período", estilo_titulo))
    elementos.append(Paragraph(
        f"Período: {data_inicio} a {data_fim} | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        estilo_sub
    ))
    elementos.append(Spacer(1, 0.5*cm))

    # ----- Resumo -----
    dados_resumo = [
        ['Total de Vendas', 'Faturamento Total', 'Ticket Médio', 'Itens Vendidos'],
        [
            str(totais['total_vendas']),
            f"R$ {totais['faturamento']:.2f}",
            f"R$ {totais['ticket_medio']:.2f}",
            str(totais['total_itens'])
        ]
    ]

    tabela_resumo = Table(dados_resumo, colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 4.5*cm])
    tabela_resumo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COR_ESCURA),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, 1), COR_CINZA),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, 1), 13),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, 1), [COR_CINZA]),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 0.5*cm))

    # ----- Título da tabela de vendas -----
    elementos.append(Paragraph("Detalhamento das Vendas", ParagraphStyle(
        'Secao', parent=styles['Heading2'], fontSize=11, textColor=COR_ESCURA, spaceBefore=6
    )))
    elementos.append(Spacer(1, 0.2*cm))

    # ----- Tabela de vendas -----
    cabecalho = ['#', 'Data / Hora', 'Cliente', 'Itens', 'Pagamento', 'Total']
    linhas = [cabecalho]

    for v in vendas:
        linhas.append([
            f'#{v.id}',
            v.data_venda.strftime('%d/%m/%Y %H:%M'),
            v.cliente.nome if v.cliente else '—',
            str(len(v.itens)),
            v.forma_pagamento.capitalize(),
            f'R$ {float(v.total):.2f}'
        ])

    tabela_vendas = Table(linhas, colWidths=[1.5*cm, 3.5*cm, 4.5*cm, 1.8*cm, 3*cm, 3*cm])
    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COR_VERDE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COR_CINZA]),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.grey),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ])
    tabela_vendas.setStyle(estilo_tabela)
    elementos.append(tabela_vendas)

    # ----- Rodapé (via onFirstPage/onLaterPages) -----
    def rodape(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(colors.grey)
        canvas.drawString(1.5*cm, 0.8*cm, 'SuperGest — Sistema de Gerenciamento de Supermercado')
        canvas.drawRightString(A4[0] - 1.5*cm, 0.8*cm, f'Página {doc.page}')
        canvas.restoreState()

    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)
    buffer.seek(0)
    return buffer
