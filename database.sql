-- ============================================================
-- SuperGest — Script de criação do banco de dados MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS supergest
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE supergest;

-- -----------------------------------------------
-- USUARIOS
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100)  NOT NULL,
    email       VARCHAR(150)  NOT NULL UNIQUE,
    senha_hash  VARCHAR(255)  NOT NULL,
    ativo       BOOLEAN       NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------
-- CATEGORIAS
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nome      VARCHAR(80)  NOT NULL UNIQUE,
    descricao VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------
-- FORNECEDORES
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS fornecedores (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    razao_social VARCHAR(150) NOT NULL,
    cnpj         CHAR(14)     NOT NULL UNIQUE,
    telefone     VARCHAR(20),
    email        VARCHAR(150)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------
-- PRODUTOS
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS produtos (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id   INT            NOT NULL,
    fornecedor_id  INT            NOT NULL,
    nome           VARCHAR(150)   NOT NULL,
    codigo_barras  VARCHAR(20)    UNIQUE,
    preco_custo    DECIMAL(10,2)  DEFAULT 0.00,
    preco_venda    DECIMAL(10,2)  NOT NULL,
    estoque_atual  INT            DEFAULT 0,
    estoque_minimo INT            DEFAULT 5,
    ativo          BOOLEAN        DEFAULT TRUE,
    FOREIGN KEY (categoria_id)  REFERENCES categorias(id),
    FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------
-- CLIENTES
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nome      VARCHAR(150) NOT NULL,
    cpf       CHAR(11)     UNIQUE,
    telefone  VARCHAR(20),
    email     VARCHAR(150)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------
-- VENDAS
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS vendas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id      INT            NULL,
    usuario_id      INT            NOT NULL,
    data_venda      DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total           DECIMAL(10,2)  NOT NULL,
    forma_pagamento VARCHAR(30)    NOT NULL,
    status          VARCHAR(20)    DEFAULT 'concluida',
    FOREIGN KEY (cliente_id)  REFERENCES clientes(id)  ON DELETE SET NULL,
    FOREIGN KEY (usuario_id)  REFERENCES usuarios(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------
-- ITENS_VENDA
-- -----------------------------------------------
CREATE TABLE IF NOT EXISTS itens_venda (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    venda_id        INT           NOT NULL,
    produto_id      INT           NOT NULL,
    quantidade      INT           NOT NULL,
    preco_unitario  DECIMAL(10,2) NOT NULL,
    subtotal        DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venda_id)   REFERENCES vendas(id)   ON DELETE CASCADE,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- DADOS INICIAIS
-- ============================================================

-- Administrador padrão
-- Senha: admin123 (hash gerado com werkzeug pbkdf2:sha256)
INSERT INTO usuarios (nome, email, senha_hash, ativo) VALUES
('Administrador',
 'admin@supergest.com.br',
 'pbkdf2:sha256:600000$salt123456789012$8d4e26ce9c95578f15012e0789ede80b6d7f36dbad9e4cc7abf77e3f4f9df62',
 TRUE);
-- ATENÇÃO: Após subir o sistema, use o script create_admin.py para criar o admin com senha correta.

-- Categorias
INSERT INTO categorias (nome, descricao) VALUES
('Laticínios',       'Leite, queijo, iogurte e derivados'),
('Bebidas',          'Sucos, refrigerantes, águas e energéticos'),
('Hortifruti',       'Frutas, legumes e verduras'),
('Padaria',          'Pães, bolos e doces'),
('Limpeza',          'Produtos de limpeza doméstica'),
('Higiene Pessoal',  'Sabonetes, shampoos e cuidados pessoais'),
('Mercearia',        'Arroz, feijão, macarrão e enlatados'),
('Carnes',           'Carnes bovinas, suínas e aves'),
('Congelados',       'Alimentos congelados e sorvetes'),
('Frios',            'Embutidos, frios e queijos fatiados');

-- Fornecedores
INSERT INTO fornecedores (razao_social, cnpj, telefone, email) VALUES
('Laticínios Sul Ltda',       '12345678000101', '(41) 3322-1100', 'contato@laticinios-sul.com.br'),
('Nestlé Brasil S.A.',        '60409075000152', '(11) 2172-2000', 'sac@nestle.com.br'),
('Ambev S.A.',                '07526557000100', '(11) 2122-1500', 'contato@ambev.com.br'),
('BRF S.A.',                  '01838723000127', '(47) 3321-5000', 'sac@brf.com.br'),
('Unilever Brasil Ltda',      '04185096000181', '(11) 3523-7000', 'sac@unilever.com.br');

-- Produtos (alguns exemplos)
INSERT INTO produtos (categoria_id, fornecedor_id, nome, codigo_barras, preco_custo, preco_venda, estoque_atual, estoque_minimo) VALUES
(1, 1, 'Leite Integral 1L',       '7891000100103', 3.20,  5.90, 120, 20),
(1, 1, 'Leite Desnatado 1L',      '7891000100110', 3.50,  6.20,   4,  5),
(1, 1, 'Leite Condensado 395g',   '7891000300103', 2.80,  4.50,   0,  5),
(2, 3, 'Água Mineral 500ml',      '7896085900102', 0.80,  2.00,  80, 20),
(2, 3, 'Refrigerante Cola 2L',    '7891991010856', 4.50,  8.50,  55, 10),
(7, 2, 'Arroz Parboilizado 5kg',  '7896069400070', 11.00, 18.99,  35, 10),
(7, 2, 'Feijão Carioca 1kg',      '7896085900200', 4.20,  7.50,  40, 10),
(7, 2, 'Macarrão Espaguete 500g', '7896085900300', 2.10,  3.90,  60, 15),
(8, 4, 'Frango Inteiro Congelado 2kg', '7893000610186', 12.00, 22.90, 18, 5),
(6, 5, 'Shampoo Anticaspa 200ml', '7891024130096', 8.00, 14.90,  25, 5);

-- Cliente de exemplo
INSERT INTO clientes (nome, cpf, telefone, email) VALUES
('Maria Souza',  '12345678901', '(41) 99901-2345', 'maria.souza@email.com'),
('João Silva',   '98765432100', '(41) 99812-3456', 'joao.silva@email.com');
