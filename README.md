# SuperGest — Sistema de Gerenciamento de Supermercado

Sistema web acadêmico desenvolvido com **Python (Flask)**, **MySQL** e **Bootstrap 5**.

---

## Tecnologias

- **Backend:** Python 3.10+ / Flask 3.0
- **ORM:** SQLAlchemy + Flask-SQLAlchemy
- **Banco de dados:** MySQL 8.0
- **Autenticação:** Flask-Login + Werkzeug (hash de senha)
- **Frontend:** Bootstrap 5.3 + Bootstrap Icons
- **PDF:** ReportLab

---

## Estrutura do Projeto

```
SUPERGEST/
├── app.py               # Ponto de entrada da aplicação
├── config.py            # Configurações (banco, secret key)
├── create_admin.py      # Script para criar o admin
├── database.sql         # Schema MySQL + dados iniciais
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente (não versionar)
│
├── models/              # Entidades do banco (SQLAlchemy ORM)
│   ├── usuario.py
│   ├── produto.py
│   ├── categoria.py
│   ├── fornecedor.py
│   ├── cliente.py
│   ├── venda.py
│   └── item_venda.py
│
├── routes/              # Blueprints Flask (rotas)
│   ├── auth.py          # Login, logout e dashboard
│   ├── produtos.py
│   ├── categorias.py
│   ├── fornecedores.py
│   ├── clientes.py
│   ├── vendas.py
│   └── relatorios.py
│
├── templates/           # HTML com Jinja2 + Bootstrap
└── utils/               # Funções auxiliares
    ├── auth.py          # Decorator login_required
    ├── validators.py    # Validação de CPF/CNPJ
    └── pdf.py           # Geração de relatório em PDF
```

---

## Instalação e Configuração

### 1. Pré-requisitos

- Python 3.10 ou superior
- MySQL 8.0 ou superior
- pip

### 2. Clonar / Baixar o projeto

```bash
# Acesse a pasta do projeto
cd SUPERGEST
```

### 3. Criar ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar o banco de dados MySQL

Acesse o MySQL e execute:

```sql
-- No terminal MySQL:
mysql -u root -p

-- Depois execute o script:
source database.sql
```

Ou importe diretamente:

```bash
mysql -u root -p < database.sql
```

### 6. Configurar variáveis de ambiente

Edite o arquivo `.env` na raiz do projeto:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=supergest_chave_secreta_2026

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=SUA_SENHA_AQUI
DB_NAME=supergest
```

### 7. Criar o usuário administrador

```bash
python create_admin.py
```

Saída esperada:
```
✓ Administrador criado/atualizado com sucesso!
  E-mail: admin@supergest.com.br
  Senha:  admin123
```

### 8. Rodar o projeto

```bash
flask run
```

ou

```bash
python app.py
```

---

## Acesso ao Sistema

Abra o navegador em:

```
http://localhost:5000
```

**Credenciais padrão:**

| Campo | Valor                         |
|-------|-------------------------------|
| Email | admin@supergest.com.br        |
| Senha | admin123                      |

> ⚠️ Altere a senha após o primeiro acesso.

---

## Funcionalidades

| Módulo       | Funcionalidades                                    |
|--------------|----------------------------------------------------|
| Login        | Autenticação com e-mail e senha, controle de sessão|
| Dashboard    | Indicadores: produtos, faturamento, estoque        |
| Produtos     | CRUD completo, busca, filtro por categoria/estoque |
| Categorias   | CRUD via modal                                     |
| Fornecedores | CRUD completo com validação de CNPJ                |
| Clientes     | CRUD completo com validação de CPF                 |
| Vendas       | Registro com múltiplos itens, desconto de estoque  |
| Relatórios   | Relatório de vendas por período + exportação PDF   |

---

## Observações Acadêmicas

- Projeto desenvolvido para fins didáticos.
- O sistema utiliza exclusão lógica para produtos (campo `ativo`).
- O estoque é atualizado automaticamente no registro de vendas.
- O relatório PDF é gerado com a biblioteca ReportLab.
- Os Blueprints do Flask organizam as rotas por domínio de negócio.
