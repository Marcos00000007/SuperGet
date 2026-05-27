from app import db

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    codigo_barras = db.Column(db.String(20), unique=True)
    preco_custo = db.Column(db.Numeric(10, 2), default=0)
    preco_venda = db.Column(db.Numeric(10, 2), nullable=False)
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=5)
    ativo = db.Column(db.Boolean, default=True)

    itens_venda = db.relationship('ItemVenda', backref='produto', lazy=True)

    @property
    def status_estoque(self):
        if self.estoque_atual == 0:
            return 'sem_estoque'
        elif self.estoque_atual <= self.estoque_minimo:
            return 'estoque_baixo'
        return 'ok'

    def __repr__(self):
        return f'<Produto {self.nome}>'
