# Reader Server

Reader Server é um servidor local de biblioteca de ebooks em Python + Flask, criado para rodar na rede Wi‑Fi local do Mac e servir leitores como XTEINK X4 Pro, KOReader, Kindle, iPhone, iPad e Mac.

## Requisitos

- Python 3.11+
- macOS Apple Silicon/M1
- rede Wi‑Fi local

## Instalação local

```bash
git clone <repository>
cd reader-server

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

Os diretórios `books/`, `covers/` e `data/` são criados para os dados de cada
instalação. Eles são ignorados pelo Git; mantenha apenas os arquivos `.gitkeep`
ao publicar o projeto.

## Executar

```bash
python run.py
```

ou:

```bash
./start.sh
```

O servidor fica disponível em:

```text
http://localhost:8080
```

Para acessar de outro dispositivo na mesma rede Wi‑Fi, descubra o endereço do Mac:

```bash
ipconfig getifaddr en0
```

Depois use:

```text
http://IP_DO_MAC:8080
```

O servidor foi projetado para uso em uma rede local confiável. Ele não possui
autenticação e não deve ser exposto diretamente à internet.

## Conteúdo da biblioteca

Não inclua ebooks, capas, bancos SQLite ou outros arquivos pessoais no
repositório. Além de poderem conter dados privados, os livros podem estar
protegidos por direitos autorais. Cada usuário deve adicionar seus próprios
arquivos à pasta `books/`.

## Estrutura

```text
reader-server/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes/
│   │   ├── main.py
│   │   ├── books.py
│   │   └── opds.py
│   ├── services/
│   │   ├── library.py
│   │   ├── metadata.py
│   │   └── covers.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── book.html
│   │   └── settings.html
│   └── static/
│       ├── css/
│       │   └── app.css
│       └── js/
│           └── app.js
├── books/
├── covers/
├── data/
├── tests/
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
├── start.sh
└── README.md
```

## Funcionalidades

- Biblioteca local em SQLite
- Importação automática de livros em pastas suportadas
- Busca por título, autor, série, ISBN e editor
- Download por livro
- Catálogo OPDS em /opds
- API JSON em /api/books
- Proteção contra path traversal
- Interface web responsiva

## Licença

Este projeto é para uso local e pessoal.
