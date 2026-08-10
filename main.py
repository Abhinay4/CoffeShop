from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import Product

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    products = Product.query.order_by(Product.sort_order).all()
    return render_template("index.html", menu=products)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)
