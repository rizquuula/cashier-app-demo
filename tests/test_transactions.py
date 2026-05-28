import json
from models import Transaction, TransactionItem, Product


class TestTransactionSection:

    def test_get_transactions_returns_200(self, client):
        resp = client.get('/transactions/')
        assert resp.status_code == 200

    def test_get_transactions_includes_product_options(self, client, products):
        resp = client.get('/transactions/')
        assert b'Coffee' in resp.data
        assert b'Tea' in resp.data
        assert b'Sandwich' in resp.data

    def test_get_transactions_excludes_zero_stock(self, client, products):
        resp = client.get('/transactions/')
        assert b'Sold Out' not in resp.data


class TestCheckout:

    def _coffee_id(self, app):
        with app.app_context():
            return Product.query.filter_by(name='Coffee').first().id

    def _tea_id(self, app):
        with app.app_context():
            return Product.query.filter_by(name='Tea').first().id

    def _sold_out_id(self, app):
        with app.app_context():
            return Product.query.filter_by(name='Sold Out').first().id

    def test_checkout_valid_creates_transaction(self, app, client, products):
        items = json.dumps([
            {'product_id': self._coffee_id(app), 'quantity': 2},
            {'product_id': self._tea_id(app), 'quantity': 1},
        ])
        resp = client.post('/transactions/checkout', data={'items_json': items})
        assert resp.status_code == 200
        assert resp.headers.get('HX-Redirect') == '/'
        with app.app_context():
            assert Transaction.query.count() == 1
            assert Transaction.query.first().total_amount == 13.5

    def test_checkout_deducts_stock(self, app, client, products):
        coffee_id = self._coffee_id(app)
        tea_id = self._tea_id(app)
        items = json.dumps([
            {'product_id': coffee_id, 'quantity': 2},
            {'product_id': tea_id, 'quantity': 1},
        ])
        client.post('/transactions/checkout', data={'items_json': items})
        with app.app_context():
            coffee = Product.query.get(coffee_id)
            tea = Product.query.get(tea_id)
            assert coffee.stock == 98
            assert tea.stock == 99

    def test_checkout_empty_cart_returns_400(self, client):
        resp = client.post('/transactions/checkout', data={'items_json': '[]'})
        assert resp.status_code == 400

    def test_checkout_insufficient_stock_returns_400(self, app, client, products):
        items = json.dumps([
            {'product_id': self._sold_out_id(app), 'quantity': 1},
        ])
        resp = client.post('/transactions/checkout', data={'items_json': items})
        assert resp.status_code == 400

    def test_checkout_insufficient_stock_rollback(self, app, client, products):
        coffee_id = self._coffee_id(app)
        sold_out_id = self._sold_out_id(app)
        items = json.dumps([
            {'product_id': coffee_id, 'quantity': 1},
            {'product_id': sold_out_id, 'quantity': 1},
        ])
        client.post('/transactions/checkout', data={'items_json': items})
        with app.app_context():
            coffee = Product.query.get(coffee_id)
            assert coffee.stock == 100

    def test_checkout_non_existent_product_returns_400(self, client):
        resp = client.post(
            '/transactions/checkout',
            data={'items_json': json.dumps([{'product_id': 999, 'quantity': 1}])},
        )
        assert resp.status_code == 400

    def test_checkout_creates_transaction_items(self, app, client, products):
        coffee_id = self._coffee_id(app)
        tea_id = self._tea_id(app)
        items = json.dumps([
            {'product_id': coffee_id, 'quantity': 2},
            {'product_id': tea_id, 'quantity': 1},
        ])
        client.post('/transactions/checkout', data={'items_json': items})
        with app.app_context():
            t = Transaction.query.first()
            assert t is not None
            item_records = TransactionItem.query.filter_by(transaction_id=t.id).all()
            assert len(item_records) == 2
            i0 = next(i for i in item_records if i.product_id == coffee_id)
            assert i0.quantity == 2
            assert i0.unit_price == 5.0
            assert i0.subtotal == 10.0
            i1 = next(i for i in item_records if i.product_id == tea_id)
            assert i1.quantity == 1
            assert i1.unit_price == 3.5
            assert i1.subtotal == 3.5


class TestTransactionLog:

    def test_log_returns_200(self, client):
        resp = client.get('/transactions/log')
        assert resp.status_code == 200

    def test_log_empty_shows_no_transactions(self, client):
        resp = client.get('/transactions/log')
        assert b'No transactions yet' in resp.data

    def test_log_shows_transactions(self, app, client, transaction_with_items):
        resp = client.get('/transactions/log')
        assert b'No transactions yet' not in resp.data
        with app.app_context():
            tx_id = str(
                Transaction.query.first().id
            ).encode()
        assert tx_id in resp.data
        assert b'17.00' in resp.data
        assert b'2 item(s)' in resp.data
