from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user

from extensions import db
from forms import CheckoutForm
from models import Order, OrderItem
from cart_utils import get_cart_lines, get_cart_total, clear_cart

checkout_bp = Blueprint("checkout", __name__, url_prefix="/checkout")


@checkout_bp.route("/", methods=["GET", "POST"])
def checkout():
    lines = get_cart_lines()
    if not lines:
        flash("Your cart is empty. Add something tasty before checking out.", "info")
        return redirect(url_for("cart.view"))

    total = get_cart_total(lines)

    form = CheckoutForm()
    if current_user.is_authenticated and not form.is_submitted():
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email

    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id if current_user.is_authenticated else None,
            full_name=form.full_name.data.strip(),
            email=form.email.data.lower().strip(),
            phone=form.phone.data.strip(),
            address_line1=form.address_line1.data.strip(),
            address_line2=(form.address_line2.data or "").strip() or None,
            city=form.city.data.strip(),
            state=form.state.data.strip(),
            postal_code=form.postal_code.data.strip(),
            payment_method=form.payment_method.data,
            total=total,
        )
        for line in lines:
            order.items.append(
                OrderItem(
                    product_id=line["product"].id,
                    product_name=line["product"].name,
                    unit_price=line["product"].price,
                    quantity=line["quantity"],
                )
            )

        db.session.add(order)
        db.session.commit()
        clear_cart()

        flash("Order placed! We're getting it ready.", "success")
        return redirect(url_for("checkout.confirmation", order_id=order.id))

    return render_template("checkout.html", form=form, lines=lines, total=total)


@checkout_bp.route("/confirmation/<int:order_id>")
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)

    # Orders placed while logged in belong to that account; anyone else
    # (including a different logged-in user) shouldn't be able to view them
    # by guessing the id. Guest orders (user_id is None) have no owner to
    # check against, so the confirmation link itself is the only "key".
    if order.user_id and (not current_user.is_authenticated or current_user.id != order.user_id):
        abort(404)

    return render_template("order_confirmation.html", order=order)
