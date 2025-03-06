from models import Product

class ProductService:
    def get_products(self, page, per_page):
        return Product.query.order_by(Product.id).paginate(page=page, per_page=per_page)
