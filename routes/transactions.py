from flask import Blueprint, render_template, request, Response, json
from models import db, Product, Transaction, TransactionItem

transactions_bp = Blueprint('transactions_bp', __name__, url_prefix='/transactions')

@transactions_bp.route('/')
def transaction_section():
    products = Product.query.filter(Product.stock > 0).all()
    return render_template('partials/transaction_section.html', products=products)

@transactions_bp.route('/checkout', methods=['POST'])
def checkout():
    items_json = request.form.get('items_json', '[]')
    items_data = json.loads(items_json)
    if not items_data:
        return Response(status=400, headers={'HX-Redirect': '/'})

    total = 0.0
    transaction = Transaction(total_amount=0.0)
    db.session.add(transaction)
    db.session.flush()

    for item in items_data:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            db.session.rollback()
            return Response(status=400, headers={'HX-Redirect': '/'})
        unit_price = product.price
        quantity = item['quantity']
        subtotal = unit_price * quantity
        total += subtotal
        product.stock -= quantity
        ti = TransactionItem(
            transaction_id=transaction.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )
        db.session.add(ti)

    transaction.total_amount = total
    db.session.commit()
    return Response(status=200, headers={'HX-Redirect': '/'})

@transactions_bp.route('/log')
def transaction_log():
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(50).all()
    return render_template('partials/transaction_log.html', transactions=transactions)
