# Ember & Bean — Coffee Shop Website

A Flask + PostgreSQL website with a landing page, user registration, and
login. Passwords are hashed with bcrypt, sessions are managed with
Flask-Login, and forms are protected with CSRF tokens via Flask-WTF.

## Project structure

```
coffeeshop/
├── app.py              # Application factory / entry point
├── config.py           # Reads settings from environment variables
├── extensions.py       # Shared Flask extension instances
├── models.py           # SQLAlchemy User & Product models
├── forms.py            # Registration & login forms with validation
├── auth.py             # Blueprint: /register, /login, /logout
├── main.py             # Blueprint: / (landing page), /dashboard
├── cart.py             # Blueprint: /cart (add, view, update, remove, clear)
├── cart_utils.py       # Session-based cart helper functions
├── seed.py             # Populates the products table with starter menu items
├── requirements.txt
├── .env.example
├── static/
│   └── css/style.css   # Responsive design system
└── templates/
    ├── base.html
    ├── index.html       # Landing page
    ├── login.html
    ├── register.html
    ├── dashboard.html
    └── 404.html
```

## 1. Prerequisites

- Python 3.10+
- PostgreSQL 13+ installed and running locally (or a hosted instance)

## 2. Create the database

```bash
# From the postgres CLI or psql shell
createdb coffeeshop
```

Or inside `psql`:

```sql
CREATE DATABASE coffeeshop;
```

## 3. Set up the project

```bash
cd coffeeshop
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Then edit .env:
#   SECRET_KEY=<generate one, e.g. `python -c "import secrets; print(secrets.token_hex(32))"`>
#   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/coffeeshop
```

## 4. Create the database tables

This project uses Flask-Migrate (a wrapper around Alembic) to manage schema
changes.

```bash
flask db init          # only once, creates the migrations/ folder
flask db migrate -m "create users table"
flask db upgrade
```

If you'd rather skip migrations for a quick local test, you can instead run:

```bash
python -c "from app import app; from extensions import db; app.app_context().push(); db.create_all()"
```

## 5. Load the starter menu into the database

The landing page now reads its menu from a `products` table instead of a
hardcoded list, so run the seed script once your tables exist:

```bash
python seed.py
```

Re-running it is safe — it updates existing rows by `slug` instead of
duplicating them.

## 6. Run the app

```bash
flask --app app run --debug
```

Visit **http://127.0.0.1:5000** — you'll land on the coffee shop homepage.
Use the **Join** button to register, then **Log in** to view the member
dashboard.

## Notes on production readiness

- Set `debug=False` and use a production WSGI server (e.g. `gunicorn app:app`).
- Set a strong, random `SECRET_KEY` and never commit `.env`.
- Put the app behind HTTPS so cookies (`SESSION_COOKIE_HTTPONLY`, etc.) are
  actually protected in transit.
- Consider adding rate limiting (e.g. Flask-Limiter) on `/login` to slow down
  brute-force attempts.
- The cart lives in the Flask **session** (a signed cookie), so it works for
  both guests and logged-in users without a database write, but it does not
  follow a person across devices or browsers. If you want a cart that
  persists per account, add a `CartItem` table keyed by `user_id` and merge
  the session cart into it on login.
- Checkout is intentionally left as a disabled button (`/cart` page) — wire
  it up to a payment processor (e.g. Stripe Checkout) and an `Order` table
  when you're ready to accept real orders.
