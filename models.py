from datetime import datetime, timezone
from decimal import Decimal

from flask_login import UserMixin

from extensions import db, login_manager, bcrypt


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    level = db.Column(db.String(40), nullable=False)       # e.g. "Light Roast"
    name = db.Column(db.String(120), nullable=False)       # e.g. "Ethiopia Yirgacheffe"
    notes = db.Column(db.String(200), nullable=False)      # tasting notes
    price = db.Column(db.Numeric(6, 2), nullable=False)
    sort_order = db.Column(db.Integer, default=0)

    def price_display(self) -> str:
        return f"{Decimal(self.price):.2f}"

    def __repr__(self) -> str:
        return f"<Product {self.slug}>"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, raw_password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))
