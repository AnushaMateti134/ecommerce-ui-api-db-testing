# E-Commerce UI API DB Testing Framework

A full-stack QA automation project demonstrating UI, API, database, and end-to-end testing using Python, Pytest, Playwright, Requests, FastAPI, SQLAlchemy, and SQLite.

## Tech Stack

- Python
- Pytest
- Playwright
- Requests
- FastAPI
- SQLAlchemy
- SQLite
- HTML Test Reports

## Test Architecture

```text
UI Tests
   ↓
Playwright Page Objects
   ↓
FastAPI Application
   ↓
API Layer
   ↓
SQLite Database

ecommerce-ui-api-db-testing/
│
├── app/
│   ├── api/
│   │   ├── users.py
│   │   ├── products.py
│   │   └── orders.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── api_clients/
│   ├── user_api.py
│   ├── product_api.py
│   └── order_api.py
│
├── pages/
│   ├── login_page.py
│   ├── products_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── db/
│   └── db_helper.py
│
├── frontend/
│   ├── index.html
│   ├── products.html
│   ├── cart.html
│   ├── checkout.html
│   ├── app.js
│   └── style.css
│
├── tests/
│   ├── api/
│   ├── db/
│   ├── ui/
│   ├── e2e/
│   └── conftest.py
│
├── config/
├── reports/
├── pytest.ini
├── requirements.txt
└── README.md

Author:
Anusha Mateti