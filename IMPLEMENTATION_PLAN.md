# Banking Web Application — Implementation Plan

> **Planning Level Document** — No schema, SQL scripts, API contracts, or implementation code.

---

## 1. Solution Overview

### 1.1 Objective

Build a single-branch, full-stack banking web application that allows customers to securely log in, view their account dashboard, check their balance, deposit funds, withdraw funds, and log out.

### 1.2 Scope

**In Scope**
- Customer authentication (login / logout)
- Personal dashboard with account summary
- Balance enquiry
- Deposit and withdrawal transactions
- Session management and route protection
- Lightweight SQLite persistence layer

**Out of Scope**
- User registration / self-service sign-up
- Multi-account support per customer
- Fund transfers between accounts
- Admin or bank-teller portal

### 1.3 Users

| User Type | Description |
|-----------|-------------|
| **Customer** | An individual with a pre-seeded bank account who uses the web interface to manage their finances |

### 1.4 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-01 | A customer must be able to log in with a username and password |
| FR-02 | Authenticated customers must be directed to a personal dashboard |
| FR-03 | The dashboard must display the customer name and current account balance |
| FR-04 | A customer must be able to deposit a positive monetary amount |
| FR-05 | A customer must be able to withdraw a positive monetary amount not exceeding the available balance |
| FR-06 | All transaction outcomes must be surfaced to the customer via on-screen feedback |
| FR-07 | A customer must be able to securely log out, invalidating their session |
| FR-08 | Unauthenticated requests to protected pages must redirect to the login page |

### 1.5 Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-01 | The UI must be responsive and render correctly on desktop and tablet viewports |
| NFR-02 | Passwords must be stored as hashed values — never plain text |
| NFR-03 | Session tokens must be invalidated on logout |
| NFR-04 | The backend must validate all inputs server-side before processing |
| NFR-05 | The application must be runnable locally with a single startup command |

### 1.6 Assumptions

- The SQLite database is pre-seeded with at least one customer account.
- The application runs on `localhost`.
- Bootstrap CDN is acceptable.

---

## 2. High-Level Architecture

### 2.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT BROWSER                           │
│   login.html  │  dashboard.html  │  transactions.html           │
└───────────────────────────┬─────────────────────────────────────┘
                            │  HTTP (form POST)
┌───────────────────────────▼─────────────────────────────────────┐
│                     FLASK BACKEND (Python)                      │
│   Auth Routes │ Account Routes │ Transaction Routes             │
└────────────────────────────┬────────────────────────────────────┘
                             │  SQLite queries
┌────────────────────────────▼────────────────────────────────────┐
│                    SQLITE DATABASE                              │
│            customers  │  accounts  │  transactions              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Design

### 3.1 Frontend Responsibilities

| Concern | Responsibility |
|---------|---------------|
| Page Rendering | Login, Dashboard, Deposit, Withdraw |
| UI Framework | Bootstrap 5 |
| Scroll & Animations | Locomotive Scroll |
| Form Handling | Login credentials and transaction amounts |
| Feedback Display | Success banners, error alerts |

### 3.2 Backend Responsibilities

| Concern | Responsibility |
|---------|---------------|
| Routing | /login, /logout, /dashboard, /deposit, /withdraw |
| Authentication | Verify hashed credentials, create/destroy sessions |
| Input Validation | Numeric, positive, within balance limits |
| Business Logic | Deposit and withdrawal rules |

### 3.3 Database Responsibilities

| Concern | Responsibility |
|---------|---------------|
| Customer Storage | Identity and hashed password |
| Account Storage | Balance linked to customer |
| Transaction Ledger | Every deposit/withdrawal with timestamp |

---

## 4. Folder Structure

```
Banking-application-Bob-demo/
├── FRONTEND/
│   ├── templates/
│   └── static/css/ static/js/
├── BACKEND/
│   ├── app.py
│   ├── config.py
│   ├── routes/
│   ├── services/
│   ├── database/
│   └── requirements.txt
└── IMPLEMENTATION_PLAN.md
```

---

## 5. Module Breakdown

### 5.1 Authentication Module
| Component | Description |
|-----------|-------------|
| Login Page | HTML form accepting username and password |
| Auth Route | /login POST, /logout GET |
| Auth Service | Queries DB, compares hashed password, manages session |
| Session Guard | Decorator redirecting unauthenticated users |

### 5.2 Dashboard Module
| Component | Description |
|-----------|-------------|
| Dashboard Page | Customer name, account number, balance |
| Dashboard Route | Protected route fetching account data |

### 5.3 Transactions Module
| Component | Description |
|-----------|-------------|
| Deposit Page | Form for positive deposit amount |
| Withdraw Page | Form validated against current balance |
| Transaction Routes | Protected POST handlers |

---

## 6. Implementation Roadmap

| Phase | Goal | Effort |
|-------|------|--------|
| 1 — Scaffold | Folder structure, venv, hello-world Flask | XS |
| 2 — Database | SQLite tables, connection helper, seed data | S |
| 3 — Auth | Login/logout, session management, route guard | S |
| 4 — Dashboard | Protected dashboard with live balance | S |
| 5 — Transactions | Deposit/withdraw with validation | S |
| 6 — UI Polish | Consistent theme, end-to-end tests | M |

> **Effort Key:** XS = < 30 min · S = 30–90 min · M = 90 min–3 hrs
