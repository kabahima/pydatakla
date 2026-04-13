# PyData Kampala Conference Website

The official website for **PyData Kampala** — a community conference bringing together data scientists, engineers, and analysts across Uganda and East Africa.

Built with [Django](https://www.djangoproject.com/).

---

## Features

- Conference schedule with rooms and time slots
- Speaker profiles
- Talk listing and detail pages
- Sponsor tiers and job board
- Code of Conduct and About pages

---

## Local Development Setup

### Prerequisites

- Python 3.11+
- [Git](https://git-scm.com/)

### 1. Clone the repository

```bash
git clone https://github.com/kabahima/pydatakla.git
cd pydatakla
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt   # dev tools (linter, pre-commit)
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env and set DJANGO_SECRET_KEY to a unique value
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. (Optional) Load sample data

```bash
python manage.py loaddata conference/fixtures/sample_data.json
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser.

---

## Running Tests

```bash
python manage.py test
```

---

## Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
ruff check .          # lint
ruff format .         # format
```

To install the pre-commit hooks so these run automatically before every commit:

```bash
pre-commit install
```

---

## Contributing

We welcome contributions of all kinds! Please read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## License

[MIT](LICENSE)
