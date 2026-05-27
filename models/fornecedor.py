from app import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(150), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(150))

    produtos = db.relationship('Produto', backref='fornecedor', lazy=True)

    def __repr__(self):
        return f'<Fornecedor {self.razao_social}>'
