from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from extensions import db
from forms import ProfileForm, ChangePasswordForm
from models import Product, Order

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    products = Product.query.order_by(Product.sort_order).all()
    return render_template("index.html", menu=products)


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
