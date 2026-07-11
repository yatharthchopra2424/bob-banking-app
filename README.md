# NexaBank — Banking Web Application

A full-stack demo banking application built with **Flask**, **SQLite**, **Bootstrap 5**, and **Locomotive Scroll**.

---

## Quick Start

### 1. Create and activate the virtual environment

```bash
cd BACKEND
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

### 4. Demo credentials

| Username | Password    |
|----------|-------------|
| `alice`  | `password123` |

---

## Run Tests

```bash
cd BACKEND
venv\Scripts\activate   # or source venv/bin/activate
pytest -v
```

All 39 tests should pass (unit + integration).

---

## Project Structure

```
Banking-application-Bob-demo/
├── FRONTEND/
│   ├── templates/          # Jinja2 HTML pages (base, login, dashboard, deposit, withdraw, errors)
│   └── static/
│       ├── css/styles.css  # Custom styles (Bootstrap + Locomotive overrides)
│       └── js/main.js      # Locomotive Scroll init + UI helpers
├── BACKEND/
│   ├── app.py              # Flask entry point
│   ├── config.py           # Environment-driven configuration
│   ├── requirements.txt    # Python dependencies
│   ├── routes/             # Blueprint route handlers (auth, dashboard, transactions)
│   ├── services/           # Business logic (auth_service, account_service)
│   ├── database/           # db.py connection helper + banking.db (auto-created)
│   └── tests/              # pytest unit + integration tests
├── IMPLEMENTATION_PLAN.md
└── STEP_BY_STEP_IMPLEMENTATION_GUIDE.md
```

---

## Features

- **Login / Logout** — session-based authentication with hashed passwords
- **Dashboard** — animated balance display with account summary
- **Deposit** — add funds with quick-amount buttons
- **Withdraw** — remove funds with overdraft protection
- **Route protection** — all non-login pages require an active session
- **Flash messages** — success/error feedback after every transaction
- **Responsive UI** — Bootstrap 5 grid, mobile-ready
- **Smooth scrolling** — Locomotive Scroll animations
