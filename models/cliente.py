from app import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(11), unique=True)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(150))

    vendas = db.relationship('Venda', backref='cliente', lazy=True)

    def __repr__(self):
        return f'<Cliente {self.nome}>'
