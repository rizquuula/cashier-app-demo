from flask import Blueprint, render_template, request, Response

products_bp = Blueprint('products_bp', __name__, url_prefix='/products')

@products_bp.route('/')
def product_list():
    from models import Product
    products = Product.query.all()
    return render_template('partials/product_list.html', products=products)

@products_bp.route('/', methods=['POST'])
def add_product():
    from models import Product, db
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    product = Product(name=name, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()
    return Response(status=200, headers={'HX-Redirect': '/'})

@products_bp.route('/<int:id>/edit')
def edit_product(id):
    from models import Product
    product = Product.query.get_or_404(id)
    return render_template('partials/product_form.html', product=product, editing=True)

@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    from models import Product, db
    product = Product.query.get_or_404(id)
    product.name = request.form['name']
    product.price = float(request.form['price'])
    product.stock = int(request.form['stock'])
    db.session.commit()
    return Response(status=200, headers={'HX-Redirect': '/'})

@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    from models import Product, db
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return Response(status=200, headers={'HX-Redirect': '/'})
