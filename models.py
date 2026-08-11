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


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line1 = db.Column(db.String(200), nullable=False)
    address_line2 = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(12), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)

    total = db.Column(db.Numeric(8, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", backref="orders")
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")

    def total_display(self) -> str:
        return f"{Decimal(self.total):.2f}"

    def __repr__(self) -> str:
        return f"<Order #{self.id}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)

    # Snapshot the name/price at time of purchase so historic orders stay
    # accurate even if the product is later renamed, repriced, or removed.
    product_name = db.Column(db.String(120), nullable=False)
    unit_price = db.Column(db.Numeric(6, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product")

    def line_total_display(self) -> str:
        return f"{Decimal(self.unit_price) * self.quantity:.2f}"

    def __repr__(self) -> str:
        return f"<OrderItem product={self.product_name} qty={self.quantity}>"


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))
