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
        slug="chikmagalur-estate",
        level="Light Roast",
        name="Chikmagalur Estate",
        notes="Cardamom, jaggery, citrus",
        price="35.00",
        sort_order=1,
    ),
    dict(
        slug="coorg-peaberry",
        level="Medium Roast",
        name="Coorg Peaberry",
        notes="Honey, orange peel, pepper",
        price="40.00",
        sort_order=2,
    ),
    dict(
        slug="araku-valley",
        level="Medium-Dark Roast",
        name="Araku Valley",
        notes="Jackfruit, dark cocoa, spice",
        price="45.00",
        sort_order=3,
    ),
    dict(
        slug="malabar-monsooned",
        level="Dark Roast",
        name="Malabar Monsooned",
        notes="Roasted chicory, molasses, smoke",
        price="50.00",
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
