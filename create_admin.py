"""
Script auxiliar para criar o usuário administrador com senha correta.
Execute APÓS criar o banco e ANTES de rodar o sistema pela primeira vez.

Uso:
    python create_admin.py
"""

from app import create_app, db
from models.usuario import Usuario

app = create_app()

with app.app_context():
    # Verifica se já existe
    admin = Usuario.query.filter_by(email='admin@supergest.com.br').first()

    if admin:
        print('Usuário admin já existe. Atualizando senha...')
        admin.set_senha('admin123')
    else:
        admin = Usuario(
            nome='Administrador',
            email='admin@supergest.com.br',
            ativo=True
        )
        admin.set_senha('admin123')
        db.session.add(admin)

    db.session.commit()
    print('✓ Administrador criado/atualizado com sucesso!')
    print('  E-mail: admin@supergest.com.br')
    print('  Senha:  admin123')
    print()
    print('⚠ Altere a senha após o primeiro acesso!')
