# Reader Server — especificação do projeto

Crie um servidor de biblioteca de ebooks usando **Python + Flask**, pensado para rodar localmente em um **MacBook Air M1** e ser acessado por outros dispositivos na mesma rede Wi-Fi.

O objetivo é criar uma alternativa simples ao `crosspoint.local`, funcionando como uma biblioteca pessoal para:

* XTEINK X4 Pro com CrossPoint
* Kindle desbloqueado com KOReader
* iPhone/iPad
* Mac

O servidor NÃO será exposto à internet.

---

## 1. Stack

Use:

* Python 3.11+
* Flask
* SQLite
* SQLAlchemy
* Jinja2
* HTML5
* CSS moderno
* JavaScript vanilla

Não usar React, Vue ou outro frontend framework.

Não usar Docker.

O projeto deve funcionar nativamente no macOS Apple Silicon/M1.

Crie:

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
│
├── books/
├── covers/
├── data/
├── tests/
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 2. Funcionamento local

O servidor deve iniciar com:

```bash
python run.py
```

ou:

```bash
./start.sh
```

Por padrão:

```text
http://0.0.0.0:8080
```

O Flask deve escutar em:

```text
0.0.0.0
```

para permitir que dispositivos na mesma rede Wi-Fi acessem o servidor.

Exemplo:

```text
Mac:
192.168.1.20

Servidor:
192.168.1.20:8080
```

No X4 Pro:

```text
http://192.168.1.20:8080
```

Não configurar HTTPS.

Não configurar domínio.

Não usar serviços externos.

Não fazer nenhuma chamada externa automaticamente.

---

# 3. Biblioteca

A pasta:

```text
books/
```

será a biblioteca principal.

O usuário poderá simplesmente copiar um EPUB para:

```text
books/
```

e o servidor deverá detectá-lo.

Também deverá existir upload pela interface web.

Formatos inicialmente suportados:

```text
.epub
.pdf
.mobi
.azw3
.cbz
.txt
```

Porém o projeto deve tratar EPUB como formato principal.

---

# 4. Banco de dados

Use SQLite.

Criar modelo `Book` com pelo menos:

```text
id
filename
filepath
title
subtitle
author
publisher
language
isbn
series
series_index
description
cover_path
file_size
file_hash
created_at
updated_at
```

Não depender do nome do arquivo para exibir o título.

---

# 5. Metadata de EPUB

Ao adicionar um EPUB, tente extrair automaticamente:

* título
* autor
* idioma
* publisher
* ISBN
* série
* número da série
* descrição
* capa

Use uma biblioteca Python apropriada para leitura de EPUB/OPF.

Caso algum campo não exista, deixar vazio.

O usuário poderá editar os metadados manualmente pela interface.

---

# 6. Capas

Extrair a capa do EPUB quando possível.

Salvar em:

```text
covers/
```

Exemplo:

```text
covers/123.jpg
```

A biblioteca deve mostrar capas reais.

Se não houver capa, mostrar um placeholder elegante baseado na primeira letra do título.

---

# 7. Interface principal

A página inicial deve parecer uma biblioteca de ebooks moderna e simples.

Mostrar:

```text
Reader Server

[ Buscar livros... ]

+ Adicionar livro

--------------------------------

Todos | Autores | Séries | Recentes

[ capa ]  [ capa ]  [ capa ]
 Hamlet    Musashi   Dune
```

Cada livro deve mostrar:

* capa
* título
* autor
* série
* formato

A interface deve funcionar bem tanto no Mac quanto no celular.

---

# 8. Página do livro

Ao clicar em um livro, mostrar:

* capa grande
* título
* autor
* série
* descrição
* idioma
* publisher
* ISBN
* formato
* tamanho do arquivo

Botões:

```text
Baixar
Editar
Excluir
```

Também mostrar:

```text
OPDS
```

caso o usuário queira copiar o endereço do catálogo.

---

# 9. Upload

Criar uma página/modal para upload.

Permitir:

```text
arrastar EPUB aqui
```

ou selecionar arquivo.

Depois do upload:

1. salvar arquivo em `books/`
2. calcular hash
3. extrair metadata
4. extrair capa
5. inserir/atualizar SQLite
6. mostrar o livro na biblioteca

Evitar duplicação usando hash SHA-256.

---

# 10. Scanner da biblioteca

Criar serviço:

```python
LibraryScanner
```

Ele deve:

1. percorrer `books/`
2. encontrar arquivos suportados
3. verificar se já estão no banco
4. importar arquivos novos
5. detectar arquivos removidos
6. atualizar metadata quando necessário

Criar botão:

```text
Scan Library
```

na interface.

Também executar um scan inicial ao iniciar o servidor.

---

# 11. OPDS

Esta é uma parte MUITO importante.

Criar um catálogo OPDS compatível com leitores de ebooks.

Endpoint:

```text
/opds
```

Também criar:

```text
/opds/search
/opds/books/<id>
/opds/download/<id>
```

O OPDS deve permitir que um cliente compatível:

1. conecte ao servidor
2. veja a biblioteca
3. pesquise livros
4. abra um livro
5. baixe o EPUB

Exemplo:

```text
http://192.168.1.20:8080/opds
```

O catálogo deve usar Atom/XML corretamente.

Usar os MIME types corretos:

```text
application/epub+zip
application/pdf
application/x-mobipocket-ebook
```

---

# 12. Download

Criar endpoint:

```text
/books/<id>/download
```

O download deve preservar o nome original do arquivo.

Não permitir path traversal.

Nunca confiar diretamente no caminho enviado pelo navegador.

---

# 13. Busca

A busca deve procurar em:

* título
* autor
* série
* ISBN
* publisher
* filename

Exemplo:

```text
/search?q=hamlet
```

A interface deve ter busca instantânea simples usando JavaScript.

---

# 14. Filtros

Adicionar filtros:

```text
Todos
EPUB
PDF
MOBI
AZW3
Autores
Séries
```

Também permitir ordenar:

```text
Título
Autor
Mais recentes
Mais antigos
```

---

# 15. Edição

Permitir editar:

```text
Título
Subtítulo
Autor
Série
Número da série
Publisher
Idioma
ISBN
Descrição
```

Não modificar o EPUB fisicamente quando o usuário editar metadata pela interface.

Os metadados personalizados ficam no SQLite.

---

# 16. Exclusão

Ao excluir:

Perguntar:

```text
Excluir apenas da biblioteca
```

ou:

```text
Excluir livro e arquivo
```

Nunca apagar automaticamente sem confirmação.

---

# 17. Segurança

Como o servidor será usado somente na LAN:

Não implementar sistema complexo de autenticação inicialmente.

Porém:

* bloquear path traversal
* validar extensões
* limitar tamanho de upload
* usar nomes de arquivos seguros
* não permitir execução de arquivos enviados
* não expor stack traces no modo produção

Configurar:

```text
MAX_CONTENT_LENGTH=500MB
```

por padrão.

---

# 18. Configuração

Criar `.env.example`:

```env
HOST=0.0.0.0
PORT=8080
BOOKS_DIR=./books
COVERS_DIR=./covers
DATABASE_URL=sqlite:///data/library.db
MAX_UPLOAD_MB=500
```

Nunca colocar `.env` no Git.

---

# 19. Health check

Criar:

```text
/health
```

Retornando:

```json
{
  "status": "ok"
}
```

---

# 20. API JSON

Além da interface HTML, criar uma pequena API:

```text
GET /api/books
GET /api/books/<id>
POST /api/books
PUT /api/books/<id>
DELETE /api/books/<id>
```

A API deve retornar JSON.

Isso permitirá futuramente criar um app mobile ou integrar outros dispositivos.

---

# 21. Arquitetura

Não colocar toda a aplicação dentro de `app.py`.

Separar:

```text
routes
services
models
templates
static
```

Usar Flask Application Factory.

Exemplo:

```python
create_app()
```

---

# 22. Testes

Criar testes com pytest para pelo menos:

* criação do banco
* importação de livro
* busca
* download
* OPDS
* proteção contra path traversal
* remoção de livro
* metadata

---

# 23. README

O README deve explicar exatamente como instalar no Mac M1.

Exemplo:

```bash
git clone <repository>
cd reader-server

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python run.py
```

Depois:

```text
http://localhost:8080
```

Para descobrir o IP do Mac:

```bash
ipconfig getifaddr en0
```

E acessar de outro dispositivo:

```text
http://IP_DO_MAC:8080
```

Explicar que todos os dispositivos precisam estar na mesma rede Wi-Fi.

---

# 24. Script start.sh

Criar:

```bash
#!/bin/bash

set -e

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install -r requirements.txt

python run.py
```

Dar permissão:

```bash
chmod +x start.sh
```

---

# 25. Integração com CrossPoint

O projeto deve ser pensado para funcionar como servidor de biblioteca independente do CrossPoint.

Não tentar implementar CrossPoint Sync neste primeiro momento.

O CrossPoint continuará responsável pela sincronização da posição de leitura.

Este servidor será responsável por:

```text
Biblioteca
   ↓
EPUB
   ↓
OPDS
   ↓
Download
```

Ou seja:

```text
Reader Server
    │
    ├── Biblioteca
    ├── Metadata
    ├── Capas
    ├── Busca
    └── OPDS
          │
          ├── X4 Pro / CrossPoint
          └── KOReader
```

---

# 26. Integração futura com KOReader

Não implementar agora a sincronização de progresso.

Porém, estruturar o projeto para futuramente suportar:

```text
KOReader Sync
```

sem precisar reescrever toda a aplicação.

Criar uma camada separada:

```text
services/
    library.py
    metadata.py
    covers.py
```

e futuramente:

```text
services/
    koreader_sync.py
```

---

# 27. Importante: não usar Calibre como backend

Não depender de Calibre.

O banco de dados principal deve ser o SQLite próprio da aplicação.

Não executar comandos do Calibre.

O objetivo é que o servidor seja:

```text
leve
simples
rápido
local
independente
```

---

# 28. UX

A interface deve ter aparência de um produto moderno, mas sem exageros.

Priorizar:

* espaço
* capas grandes
* tipografia limpa
* poucos botões
* navegação simples
* responsividade

Usar CSS próprio.

Não adicionar frameworks frontend desnecessários.

---

# 29. Resultado esperado

Depois de executar:

```bash
./start.sh
```

deve ser possível abrir no Mac:

```text
http://localhost:8080
```

e no X4 Pro:

```text
http://IP_DO_MAC:8080
```

Na página será possível:

1. adicionar EPUB
2. visualizar biblioteca
3. pesquisar
4. editar metadata
5. visualizar capa
6. baixar livro
7. acessar catálogo OPDS

O objetivo final é ter um **servidor pessoal de ebooks local**, funcionando como uma biblioteca central para o X4 Pro e Kindle/KOReader, sem depender de serviços externos ou da internet.
