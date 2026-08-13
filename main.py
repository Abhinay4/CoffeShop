from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from extensions import db
from forms import ProfileForm, ChangePasswordForm
from models import Product, Order, Rating

main_bp = Blueprint("main", __name__)


def _best_rated_product(products):
    """Pick the coffee to feature: highest average rating (ties broken by
    rating count), falling back to the first item on the menu if nothing
    has been rated yet — so there's always something to recommend."""
    rated = [p for p in products if p.rating_count() > 0]
    if rated:
        return max(rated, key=lambda p: (p.average_rating(), p.rating_count()))
    return products[0] if products else None


@main_bp.route("/")
def index():
    products = Product.query.order_by(Product.sort_order).all()
    best = _best_rated_product(products)
    return render_template("index.html", menu=products, best=best)


@main_bp.route("/rate/<int:product_id>", methods=["POST"])
def rate_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        stars = int(request.form.get("stars", 0))
    except ValueError:
        stars = 0

    if stars < 1 or stars > 5:
        flash("Please choose a rating between 1 and 5 stars.", "danger")
    else:
        db.session.add(Rating(product_id=product.id, stars=stars))
        db.session.commit()
        flash(f"Thanks for rating {product.name}!", "success")

    next_page = request.form.get("next") or request.referrer
    return redirect(next_page or url_for("main.index"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = ProfileForm(original_email=current_user.email, obj=current_user)
    password_form = ChangePasswordForm()

    if "save" in request.form and profile_form.validate_on_submit():
        current_user.full_name = profile_form.full_name.data.strip()
        current_user.email = profile_form.email.data.lower().strip()
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("main.profile"))

    if "change_password" in request.form and password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash("Current password is incorrect.", "danger")
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash("Password updated.", "success")
            return redirect(url_for("main.profile"))

    return render_template(
        "profile.html",
        profile_form=profile_form,
        password_form=password_form,
        user=current_user,
    )


@main_bp.route("/orders")
@login_required
def order_history():
    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("order_history.html", orders=orders)
