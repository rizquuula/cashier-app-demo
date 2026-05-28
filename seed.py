from app import create_app
from models import db, Product

app = create_app()
with app.app_context():
    db.create_all()
    if not Product.query.first():
        products = [
            Product(name='Coffee', price=5.0, stock=100),
            Product(name='Tea', price=3.5, stock=100),
            Product(name='Sandwich', price=12.0, stock=50),
            Product(name='Croissant', price=4.5, stock=60),
            Product(name='Water', price=2.0, stock=200),
            Product(name='Juice', price=6.0, stock=80),
            Product(name='Cookie', price=3.0, stock=150),
            Product(name='Muffin', price=4.0, stock=40),
        ]
        db.session.add_all(products)
        db.session.commit()
        print('Seed data inserted')
    else:
        print('Data already exists')
