from app import db
from datetime import datetime

class Venda(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(20), default='concluida')

    itens = db.relationship('ItemVenda', backref='venda', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Venda #{self.id}>'
