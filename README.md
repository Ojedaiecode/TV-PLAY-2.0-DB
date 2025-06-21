# Quartel-General API

Este projeto é uma API escalável construída com Python e Flask, servindo como núcleo de comunicação e operações para o Quartel-General. Desenvolvido com foco em segurança, modularização e fácil manutenção.

## 🏗️ Estrutura do Projeto

```
.
├── app/                            # Diretório principal da aplicação
│   ├── routes/                     # Rotas da aplicação
│   │   ├── main.py                # Rotas da página inicial
│   │   ├── login.py               # Sistema de autenticação
│   │   ├── home.py                # Rotas do dashboard
│   │   └── avatar.py              # Sistema de upload de avatares
│   │
│   ├── templates/                  # Templates HTML
│   │   ├── index.html             # Página inicial/login
│   │   └── home.html              # Dashboard do usuário
│   │
│   ├── static/                     # Arquivos estáticos
│   │   ├── css/                   # Estilos CSS
│   │   │   ├── index.css          # Estilos da página inicial
│   │   │   └── home.css           # Estilos do dashboard
│   │   │
│   │   └── js/                    # Scripts JavaScript
│   │       ├── index.js           # Scripts da página inicial
│   │       └── home.js            # Scripts do dashboard
│   │
│   ├── __init__.py                # Inicialização do Flask e blueprints
│   └── config.py                  # Configurações da aplicação
│
├── requirements.txt                # Dependências do projeto
├── run.py                         # Arquivo de inicialização
├── Procfile                       # Configuração para deploy no Railway
└── .gitignore                     # Arquivos ignorados pelo git
```

## ✨ Funcionalidades Implementadas

### 🔐 Autenticação
- Sistema de login/logout completo
- Proteção de rotas via sessão
- Criptografia de senhas com bcrypt
- Configurações de segurança para cookies de sessão
- Proteção contra XSS e CSRF

### 🗄️ Banco de Dados
- Integração completa com Supabase
- Gestão de usuários
- Armazenamento seguro de senhas
- Sistema de avatares

### 👤 Gestão de Usuários
- Upload de avatares para Supabase Storage
- Perfis de usuário personalizáveis
- Sistema de sessões seguro

### 🎨 Interface
- Design responsivo
- Estilização moderna com TailwindCSS
- Templates Jinja2 otimizados
- Dashboard interativo
- Menu lateral funcional

### 🛡️ Segurança
- Proteção contra XSS
- Proteção contra CSRF
- Cookies seguros (HTTPOnly, SameSite, Secure)
- Senhas criptografadas com bcrypt
- Validação de uploads

## 🚀 Deploy

O projeto está configurado para deploy no Railway através do arquivo `Procfile`:

```
web: python run.py
```

## 📦 Dependências

As principais dependências do projeto estão no `requirements.txt`:
- Flask
- python-dotenv
- supabase
- bcrypt
- Werkzeug
- outras dependências de segurança

## 🔧 Configuração

O projeto utiliza variáveis de ambiente para configuração segura:
- Integração com Supabase
- Chaves secretas
- Configurações de ambiente
- Configurações de segurança

## 💻 Desenvolvimento

O projeto segue as melhores práticas de desenvolvimento:
- Código limpo e documentado
- Modularização via Blueprints
- JavaScript para interatividade
- CSS puro para estilos

---

> **Nota:** O projeto está totalmente funcional e pronto para produção, com todas as funcionalidades de autenticação, banco de dados e interface implementadas e testadas. 