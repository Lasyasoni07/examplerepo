from flask import Flask
from config import Config
from models import db, Product, User
from controllers.auth import auth_bp
from controllers.products import products_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            for i in range(1, 21): 
                product = Product(
                    name=f"Product {i}",
                    description=f"Description for product {i}",
                    price=10 * i
                )
                db.session.add(product)
            db.session.commit()
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
