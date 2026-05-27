from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    produtos = db.relationship('Produto', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nome}>'
