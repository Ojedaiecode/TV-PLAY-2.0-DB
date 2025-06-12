# Quartel-General API

Este projeto é uma API escalável construída com Python e Flask, servindo como núcleo de comunicação e operações para o Quartel-General. Pensado para fácil expansão, modularização e implantação em ambientes como o Railway.

## Estrutura Inicial

- `app/` — Código principal da aplicação Flask
  - `routes/` — Rotas organizadas por módulos
  - `templates/` — Templates HTML (Jinja2)
  - `static/` — Arquivos estáticos (CSS, JS, imagens)
    - `css/` — Estilos da aplicação
    - `js/` — Scripts JavaScript
  - `__init__.py` — Inicialização da aplicação Flask
- `run.py` — Ponto de entrada da aplicação
- `requirements.txt` — Dependências do projeto

## Como funciona

A estrutura foi desenhada para facilitar a adição de novos módulos, rotas e integrações futuras, mantendo o código limpo e organizado.

## Atualizações Recentes

- Criado o arquivo `index.css` na pasta `static/css/`  
  ➤ Estiliza a página inicial (`index.html`) com fundo preto e texto centralizado em branco indicando "QG Painel Admin em construção".

- Criado o arquivo `index.js` na pasta `static/js/`  
  ➤ Por enquanto está vazio, mas reservado para funcionalidades futuras da tela de login/admin.

Estas adições fazem parte da estrutura base que será exibida no deploy inicial no Railway, e já preparam o projeto para futura integração com o Supabase.

---

> **Observação:** Este projeto está pronto para ser implantado no Railway e não será executado localmente durante o desenvolvimento inicial.

## Deploy (Railway)

Este projeto está configurado para ser implantado no Railway utilizando um arquivo `Procfile` com o seguinte comando:

```
web: python run.py
```

Esse comando garante que a aplicação Flask será iniciada corretamente após o deploy. 