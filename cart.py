from flask import Blueprint, render_template, redirect, url_for, flash, request, abort

from app import csrf
from models import Product
from cart_utils import (
    add_to_cart,
    set_quantity,
    remove_from_cart,
    clear_cart,
    get_cart_lines,
    get_cart_total,
)

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@csrf.exempt
def add(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        quantity = 1
    quantity = max(1, min(quantity, 20))  # sane bounds

    add_to_cart(product_id, quantity)
    flash(f"Added {product.name} to your cart.", "success")

    next_page = request.form.get("next") or request.referrer
    return redirect(next_page or url_for("main.index"))


@cart_bp.route("/")
def view():
    lines = get_cart_lines()
    total = get_cart_total(lines)
    return render_template("cart.html", lines=lines, total=total)


@cart_bp.route("/update/<int:product_id>", methods=["POST"])
@csrf.exempt
def update(product_id):
    Product.query.get_or_404(product_id)

    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        quantity = 1
    quantity = max(0, min(quantity, 20))

    set_quantity(product_id, quantity)
    return redirect(url_for("cart.view"))


@cart_bp.route("/remove/<int:product_id>", methods=["POST"])
@csrf.exempt
def remove(product_id):
    remove_from_cart(product_id)
    flash("Item removed from your cart.", "info")
    return redirect(url_for("cart.view"))


@cart_bp.route("/clear", methods=["POST"])
@csrf.exempt
def clear():
    clear_cart()
    flash("Cart cleared.", "info")
    return redirect(url_for("cart.view"))
