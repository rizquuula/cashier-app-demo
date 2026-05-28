# Cashier App Demo

A Flask-based point-of-sale (POS) application with product management, transaction processing, and sales dashboard.

## Features

- **Products** – CRUD operations for inventory management
- **Transactions** – Create and view sales transactions with line items
- **Dashboard** – Sales overview and chart visualizations
- **SQLite** – Lightweight database, no external setup required

## Quick Start

```bash
# Create virtualenv and install dependencies
make

# Seed sample products
make seed

# Run the app
make run
```

Open http://localhost:5000 in your browser.

## Available Commands

| Command | Description |
|---|---|
| `make` | Create venv + install dependencies |
| `make run` | Start the Flask dev server |
| `make seed` | Insert sample product data |
| `make test` | Run tests with pytest |
| `make init-db` | Create database tables |
| `make db-clean` | Reset the database |

## Project Structure

```
.
├── app.py              # Flask app factory
├── models.py           # SQLAlchemy models (Product, Transaction, TransactionItem)
├── seed.py             # Sample data seeder
├── routes/
│   ├── dashboard.py    # Dashboard endpoint
│   ├── products.py     # Product CRUD endpoints
│   └── transactions.py # Transaction endpoints
├── templates/          # HTML templates (Jinja2)
├── tests/              # Pytest test suite
├── requirements.txt
└── Makefile
```

## Stack

- **Flask 3.1** – Web framework
- **Flask-SQLAlchemy 3.1** – ORM
- **SQLite** – Database
- **pytest** – Testing
