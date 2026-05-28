from flask import Blueprint, render_template, jsonify
from models import db, Product, Transaction
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/')

@dashboard_bp.route('/')
def index():
    labels = []
    data = []
    today = datetime.utcnow().date()
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        label = day.strftime('%a')
        labels.append(label)
        day_start = datetime(day.year, day.month, day.day)
        day_end = day_start + timedelta(days=1)
        total = db.session.query(db.func.coalesce(db.func.sum(Transaction.total_amount), 0))\
            .filter(Transaction.created_at >= day_start, Transaction.created_at < day_end).scalar()
        data.append(float(total))
    chart_data = json.dumps({"labels": labels, "data": data})
    products = Product.query.all()
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(50).all()
    return render_template('index.html', chart_data=chart_data, products=products, transactions=transactions)

@dashboard_bp.route('/chart')
def chart():
    today = datetime.utcnow().date()
    labels = []
    data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%a'))
        day_start = datetime(day.year, day.month, day.day)
        day_end = day_start + timedelta(days=1)
        total = db.session.query(db.func.coalesce(db.func.sum(Transaction.total_amount), 0))\
            .filter(Transaction.created_at >= day_start, Transaction.created_at < day_end).scalar()
        data.append(float(total))
    chart_data = json.dumps({"labels": labels, "data": data})
    return render_template('partials/chart.html', chart_data=chart_data)

@dashboard_bp.route('/chart/data')
def chart_data():
    today = datetime.utcnow().date()
    labels = []
    data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%a'))
        day_start = datetime(day.year, day.month, day.day)
        day_end = day_start + timedelta(days=1)
        total = db.session.query(db.func.coalesce(db.func.sum(Transaction.total_amount), 0))\
            .filter(Transaction.created_at >= day_start, Transaction.created_at < day_end).scalar()
        data.append(float(total))
    return jsonify({"labels": labels, "data": data})
