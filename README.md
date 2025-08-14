# 📌 Portfólio Pessoal com Flask

Este é um site completo de portfólio pessoal desenvolvido com **Flask**, contendo autenticação de usuários, painel administrativo para gerenciamento de conteúdo e páginas públicas para exibição de projetos e conquistas.

A aplicação conta com:
- Sistema de autenticação completo (login, cadastro e recuperação de senha)
- Painel administrativo para gerenciar projetos e conquistas
- Páginas públicas interativas com curtidas e comentários
- Interface 100% em português com **tema escuro responsivo** otimizado para o ambiente **Replit**

---

## 🖥 Visão Geral

O objetivo do projeto é oferecer uma plataforma pessoal para apresentação de trabalhos e conquistas, com controle total pelo administrador e interação de visitantes.

---

## ⚙ Arquitetura do Sistema

### Frontend
- **Template Engine:** Jinja2 com Flask (renderização no servidor)
- **UI Framework:** Bootstrap 5 (tema escuro do Replit)
- **Ícones:** Font Awesome
- **JavaScript:** Vanilla JS para rolagem suave, destaques no menu, validação de formulários e animações
- **Estilo:** CSS customizado com variáveis, gradientes e design responsivo
- **Idioma:** Português (pt-BR)

### Backend
- **Framework Web:** Flask com SQLAlchemy ORM
- **Autenticação:** Login, registro, recuperação de senha, hash de senhas com Werkzeug e controle de acesso por função (admin/usuário)
- **Uploads:** Manipulação segura de arquivos (projetos e conquistas)
- **Formulários:** WTForms com proteção CSRF
- **Sessões:** Flask sessions com suporte a sessões permanentes
- **Tratamento de Erros:** Páginas personalizadas (404/500) e logs de exceções
- **Middleware:** ProxyFix para URLs HTTPS corretas em produção
- **Estrutura Modular:** Uso de `extensions.py` para evitar importações circulares

---

## 🗄 Modelos do Banco de Dados

- **Usuário:** id, nome, email, senha_hash, foto_url, is_admin, criado_em, reset_token, reset_token_expires
- **Projeto:** id, título, descrição, imagem_url, tags, status, likes_count, criado_em, atualizado_em, user_id
- **Conquista:** id, título, descrição, data, imagem_url, user_id
- **Comentário:** id, conteúdo, criado_em, user_id, project_id
- **Curtida:** id, user_id, project_id (única por usuário)
- **Notificação:** id, tipo ('like'/'comment'), mensagem, lida, criado_em, user_id

---

## 🔐 Segurança e Configuração

- Variáveis de ambiente para **URL do banco** e **chave secreta**
- Pool de conexões do SQLAlchemy
- Middleware ProxyFix para compatibilidade com reverse proxies
- Upload seguro de imagens

---

## 📦 Dependências

### Frontend
- **Bootstrap 5**
- **Font Awesome 6.4.0**
- **CSS customizado**

### Backend
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- WTForms
- SQLAlchemy
- Werkzeug
- email-validator

---

## 💾 Banco de Dados

- **SQLite** (`portfolio.db`) como banco padrão
- Relacionamentos completos com **chaves estrangeiras** e **cascade delete**
- Criação automática das tabelas no início da aplicação

---

## ☁ Hospedagem e Deploy

- **Otimizado para Replit**
- **HTTPS** via ProxyFix
- Configuração por **variáveis de ambiente**
- Armazenamento local de imagens em `static/uploads`
- Conta admin padrão:  
Email: admin@portfolio.com
Senha: admin123


---

## 📅 Últimas Atualizações (12/08/2025)

- ✅ Correção de imports circulares (`extensions.py`)
- ✅ Autenticação completa (registro, login, logout, recuperação de senha)
- ✅ Painel admin com CRUD de projetos e conquistas
- ✅ Páginas públicas interativas com curtidas/comentários
- ✅ Sistema de notificações para o admin
- ✅ Upload seguro de imagens
- ✅ Dados de exemplo (3 projetos, 2 conquistas)
- ✅ Tratamento de erros com páginas personalizadas
- ✅ Menu dinâmico com links exclusivos para admin

---

## 🚀 Como Executar Localmente

# Clonar repositório
git clone https://github.com/SEU_USUARIO/PortfolioFlask.git
cd PortfolioFlask

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python app.py
Acesse em: http://localhost:5000
