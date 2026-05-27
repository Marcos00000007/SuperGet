from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar o sistema.'
    login_manager.login_message_category = 'warning'

    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.produtos import produtos_bp
    from routes.categorias import categorias_bp
    from routes.fornecedores import fornecedores_bp
    from routes.clientes import clientes_bp
    from routes.vendas import vendas_bp
    from routes.relatorios import relatorios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(fornecedores_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(relatorios_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
