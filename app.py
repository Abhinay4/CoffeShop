from flask import Flask, render_template

from config import Config
from extensions import db, bcrypt, login_manager, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from auth import auth_bp
    from main import main_bp
    from cart import cart_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(cart_bp)

    @app.context_processor
    def inject_cart_count():
        from cart_utils import cart_item_count
        return {"cart_count": cart_item_count()}

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
