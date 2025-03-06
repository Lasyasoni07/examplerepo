from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from services.product_service import ProductService

products_bp = Blueprint('products', __name__)

@products_bp.route('/products')
def product_list():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('products.html')

@products_bp.route('/api/products', methods=['POST'])
def api_product_list():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    page = request.json.get('page', 1)
    per_page = 5
    pagination = ProductService().get_products(page, per_page)
    products = pagination.items
    total_pages = pagination.pages

    data = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price
    } for product in products]

    return jsonify({
        'products': data,
        'total_pages': total_pages
    })
