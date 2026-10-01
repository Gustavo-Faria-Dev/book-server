# Reader Server

Reader Server is a local ebook library server built with Python and Flask. It runs on a Mac and serves readers such as XTEINK X4 Pro, KOReader, Kindle, iPhone, iPad, and Mac devices on the same Wi-Fi network.

## Requirements

- Python 3.11 or newer
- macOS on Apple Silicon or Intel
- A local Wi-Fi network

## Local installation

```bash
git clone <repository>
cd reader-server

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

The `books/`, `covers/`, and `data/` directories hold data for each local
installation. They are ignored by Git; keep only the `.gitkeep` files when
publishing the project.

## Run

```bash
python run.py
```

Or:

```bash
./start.sh
```

The server is available at:

```text
http://localhost:8080
```

To access it from another device on the same Wi-Fi network, find the Mac's IP address:

```bash
ipconfig getifaddr en0
```

Then use:

```text
http://MAC_IP_ADDRESS:8080
```

The server is designed for use on a trusted local network. It has no
authentication and must not be exposed directly to the internet.

## Library content

Do not add ebooks, covers, SQLite databases, or other personal files to the
repository. They may contain private data, and ebooks may be protected by
copyright. Each user should add their own files to the `books/` directory.

## Project structure

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

## Features

- Local SQLite library
- Automatic import of supported books from the library folder
- Search by title, author, series, ISBN, and publisher
- Per-book downloads
- OPDS catalog at `/opds`
- JSON API at `/api/books`
- Path traversal protection
- Responsive web interface

## License

This project is intended for local and personal use.
