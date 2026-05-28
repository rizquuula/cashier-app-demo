from models import Product, Transaction, TransactionItem


class TestProductModel:

    def test_create_product(self, app, db):
        with app.app_context():
            p = Product(name='Croissant', price=4.5, stock=30)
            db.session.add(p)
            db.session.commit()
            saved = db.session.get(Product, p.id)
            assert saved is not None
            assert saved.name == 'Croissant'
            assert saved.price == 4.5
            assert saved.stock == 30
            assert saved.created_at is not None

    def test_default_stock(self, app, db):
        with app.app_context():
            p = Product(name='Muffin', price=2.5)
            db.session.add(p)
            db.session.flush()
            assert p.stock == 0

    def test_attributes_accessible(self, app, db):
        with app.app_context():
            p = Product(name='Brownie', price=3.0, stock=10)
            db.session.add(p)
            db.session.commit()
            assert p.id is not None
            assert str(p.name) == 'Brownie'
            assert float(p.price) == 3.0

    def test_query_by_id_and_name(self, app, db, products):
        with app.app_context():
            coffee = db.session.merge(products[0])
            by_id = db.session.get(Product, coffee.id)
            assert by_id is not None
            assert by_id.name == 'Coffee'
            by_name = db.session.execute(
                db.select(Product).filter_by(name='Coffee')
            ).scalar_one()
            assert by_name.id == coffee.id

    def test_price_with_decimals(self, app, db):
        with app.app_context():
            p = Product(name='Latte', price=4.99, stock=50)
            db.session.add(p)
            db.session.commit()
            assert p.price == 4.99

    def test_multiple_products_created(self, app, db, products):
        with app.app_context():
            count = db.session.query(Product).count()
            assert count == 4


class TestTransactionModel:

    def test_create_transaction(self, app, db):
        with app.app_context():
            t = Transaction(total_amount=25.0)
            db.session.add(t)
            db.session.commit()
            saved = db.session.get(Transaction, t.id)
            assert saved is not None
            assert saved.total_amount == 25.0

    def test_default_total_amount(self, app, db):
        with app.app_context():
            t = Transaction()
            db.session.add(t)
            db.session.flush()
            assert t.total_amount == 0.0

    def test_created_at_auto_set(self, app, db):
        with app.app_context():
            t = Transaction(total_amount=10.0)
            db.session.add(t)
            db.session.commit()
            assert t.created_at is not None

    def test_transaction_items_relationship(self, app, db, transaction_with_items):
        with app.app_context():
            t = db.session.merge(transaction_with_items)
            assert len(t.items) == 2
            assert t.items[0].product.name == 'Coffee'
            assert t.items[1].product.name == 'Tea'

    def test_delete_cascade_items(self, app, db, transaction_with_items):
        with app.app_context():
            t_id = db.session.merge(transaction_with_items).id
            items_count_before = db.session.query(TransactionItem).filter_by(transaction_id=t_id).count()
            assert items_count_before == 2
            t = db.session.get(Transaction, t_id)
            db.session.delete(t)
            db.session.commit()
            items_count_after = db.session.query(TransactionItem).filter_by(transaction_id=t_id).count()
            assert items_count_after == 0
            assert db.session.get(Transaction, t_id) is None

    def test_transaction_no_items(self, app, db):
        with app.app_context():
            t = Transaction(total_amount=0.0)
            db.session.add(t)
            db.session.commit()
            assert len(t.items) == 0


class TestTransactionItemModel:

    def test_create_transaction_item(self, app, db, products):
        with app.app_context():
            product = db.session.merge(products[0])
            t = Transaction(total_amount=10.0)
            db.session.add(t)
            db.session.flush()
            ti = TransactionItem(
                transaction_id=t.id, product_id=product.id,
                quantity=2, unit_price=5.0, subtotal=10.0
            )
            db.session.add(ti)
            db.session.commit()
            saved = db.session.get(TransactionItem, ti.id)
            assert saved is not None
            assert saved.quantity == 2
            assert saved.unit_price == 5.0
            assert saved.subtotal == 10.0

    def test_product_relationship(self, app, db, transaction_with_items):
        with app.app_context():
            t = db.session.merge(transaction_with_items)
            item = t.items[0]
            assert item.product is not None
            assert item.product.name == 'Coffee'
            assert item.product.price == 5.0

    def test_transaction_relationship(self, app, db, transaction_with_items):
        with app.app_context():
            t = db.session.merge(transaction_with_items)
            item = t.items[0]
            assert item.transaction is not None
            assert item.transaction.id == t.id
            assert item.transaction.total_amount == 17.0

    def test_subtotal_stored_as_provided(self, app, db, products):
        with app.app_context():
            product = db.session.merge(products[0])
            t = Transaction(total_amount=5.0)
            db.session.add(t)
            db.session.flush()
            ti = TransactionItem(
                transaction_id=t.id, product_id=product.id,
                quantity=1, unit_price=5.0, subtotal=5.0
            )
            db.session.add(ti)
            db.session.commit()
            assert ti.subtotal == 5.0
