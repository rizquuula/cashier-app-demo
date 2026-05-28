import pytest
from models import Product


class TestProductList:
    def test_get_products_returns_all_products(self, client, products, app):
        resp = client.get('/products/')
        assert resp.status_code == 200
        with app.app_context():
            for p in Product.query.all():
                assert p.name.encode() in resp.data

    def test_get_products_shows_empty_state(self, client, app):
        with app.app_context():
            Product.query.delete()
        resp = client.get('/products/')
        assert resp.status_code == 200
        assert b'No products yet' in resp.data


class TestCreateProduct:
    def test_post_creates_product_and_redirects(self, client, app):
        resp = client.post('/products/', data={'name': 'Latte', 'price': '4.5', 'stock': '30'})
        assert resp.status_code == 200
        assert resp.headers.get('HX-Redirect') == '/'
        with app.app_context():
            p = Product.query.filter_by(name='Latte').first()
            assert p is not None
            assert p.price == 4.5
            assert p.stock == 30


class TestEditProduct:
    def test_get_edit_returns_200(self, client, products, app):
        with app.app_context():
            pid = Product.query.first().id
        resp = client.get(f'/products/{pid}/edit')
        assert resp.status_code == 200
        assert b'Save' in resp.data

    def test_get_edit_returns_404_for_missing(self, client):
        resp = client.get('/products/9999/edit')
        assert resp.status_code == 404


class TestUpdateProduct:
    def test_put_updates_product_and_redirects(self, client, products, app):
        with app.app_context():
            pid = Product.query.first().id
        resp = client.put(f'/products/{pid}', data={'name': 'Mocha', 'price': '5.5', 'stock': '20'})
        assert resp.status_code == 200
        assert resp.headers.get('HX-Redirect') == '/'
        with app.app_context():
            p = Product.query.get(pid)
            assert p.name == 'Mocha'
            assert p.price == 5.5
            assert p.stock == 20

    def test_put_returns_404_for_missing(self, client):
        resp = client.put('/products/9999', data={'name': 'x', 'price': '1', 'stock': '1'})
        assert resp.status_code == 404


class TestDeleteProduct:
    def test_delete_removes_product_and_redirects(self, client, products, app):
        with app.app_context():
            pid = Product.query.first().id
        resp = client.delete(f'/products/{pid}')
        assert resp.status_code == 200
        assert resp.headers.get('HX-Redirect') == '/'
        with app.app_context():
            assert Product.query.get(pid) is None

    def test_delete_returns_404_for_missing(self, client):
        resp = client.delete('/products/9999')
        assert resp.status_code == 404
