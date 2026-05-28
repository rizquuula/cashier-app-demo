import pytest
from app import create_app
from models import db as _db, Product, Transaction, TransactionItem


@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        _db.create_all()
    yield app
    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db


@pytest.fixture
def products(app):
    with app.app_context():
        items = [
            Product(name='Coffee', price=5.0, stock=100),
            Product(name='Tea', price=3.5, stock=100),
            Product(name='Sandwich', price=12.0, stock=50),
            Product(name='Sold Out', price=1.0, stock=0),
        ]
        _db.session.add_all(items)
        _db.session.commit()
        return items


@pytest.fixture
def transaction_with_items(app, products):
    with app.app_context():
        p1 = _db.session.merge(products[0])
        p2 = _db.session.merge(products[1])
        t = Transaction(total_amount=17.0)
        _db.session.add(t)
        _db.session.flush()
        items = [
            TransactionItem(transaction_id=t.id, product_id=p1.id, quantity=2, unit_price=5.0, subtotal=10.0),
            TransactionItem(transaction_id=t.id, product_id=p2.id, quantity=2, unit_price=3.5, subtotal=7.0),
        ]
        _db.session.add_all(items)
        _db.session.commit()
        return t
