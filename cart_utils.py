from decimal import Decimal

from flask import session

from models import Product

CART_SESSION_KEY = "cart"


def _get_raw_cart() -> dict:
    """Cart stored as {product_id_str: quantity_int} in the session."""
    return session.setdefault(CART_SESSION_KEY, {})


def add_to_cart(product_id: int, quantity: int = 1) -> None:
    cart = _get_raw_cart()
    key = str(product_id)
    cart[key] = cart.get(key, 0) + quantity
    session.modified = True


def set_quantity(product_id: int, quantity: int) -> None:
    cart = _get_raw_cart()
    key = str(product_id)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    session.modified = True


def remove_from_cart(product_id: int) -> None:
    cart = _get_raw_cart()
    cart.pop(str(product_id), None)
    session.modified = True


def clear_cart() -> None:
    session[CART_SESSION_KEY] = {}
    session.modified = True


def cart_item_count() -> int:
    return sum(_get_raw_cart().values())


def get_cart_lines() -> list[dict]:
    """
    Resolves the session cart against the database and returns display-ready
    rows. Silently drops any product ids that no longer exist (e.g. removed
    from the catalog) so a stale cart never crashes the page.
    """
    cart = _get_raw_cart()
    if not cart:
        return []

    product_ids = [int(pid) for pid in cart.keys()]
    products = {p.id: p for p in Product.query.filter(Product.id.in_(product_ids)).all()}

    lines = []
    stale_ids = []
    for pid_str, qty in cart.items():
        product = products.get(int(pid_str))
        if not product:
            stale_ids.append(pid_str)
            continue
        line_total = Decimal(product.price) * qty
        lines.append(
            {
                "product": product,
                "quantity": qty,
                "line_total": f"{line_total:.2f}",
            }
        )

    if stale_ids:
        for pid_str in stale_ids:
            cart.pop(pid_str, None)
        session.modified = True

    lines.sort(key=lambda line: line["product"].sort_order)
    return lines


def get_cart_total(lines: list[dict] | None = None) -> str:
    if lines is None:
        lines = get_cart_lines()
    total = sum(Decimal(line["line_total"]) for line in lines)
    return f"{total:.2f}"
