"""
One-off script to populate the products table.

Run after your database tables exist:

    flask --app app shell
    >>> exec(open('seed.py').read())

Or more simply, from the project root with the venv active:

    python seed.py
"""

from app import app
from extensions import db
from models import Product

SEED_PRODUCTS = [
    dict(
        slug="ethiopia-yirgacheffe",
        level="Light Roast",
        name="Ethiopia Yirgacheffe",
        notes="Jasmine, bergamot, honey",
        price="4.50",
        sort_order=1,
    ),
    dict(
        slug="colombia-huila",
        level="Medium Roast",
        name="Colombia Huila",
        notes="Brown sugar, red apple, cocoa",
        price="4.75",
        sort_order=2,
    ),
    dict(
        slug="sumatra-mandheling",
        level="Medium-Dark Roast",
        name="Sumatra Mandheling",
        notes="Cedar, dark chocolate, earth",
        price="4.95",
        sort_order=3,
    ),
    dict(
        slug="house-espresso-blend",
        level="Dark Roast",
        name="House Espresso Blend",
        notes="Toasted hazelnut, molasses, smoke",
        price="5.25",
        sort_order=4,
    ),
]


def run():
    with app.app_context():
        for item in SEED_PRODUCTS:
            existing = Product.query.filter_by(slug=item["slug"]).first()
            if existing:
                for key, value in item.items():
                    setattr(existing, key, value)
            else:
                db.session.add(Product(**item))
        db.session.commit()
        print(f"Seeded {len(SEED_PRODUCTS)} products.")


if __name__ == "__main__":
    run()
