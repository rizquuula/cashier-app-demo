import json
from datetime import datetime

from flask import template_rendered


class TestDashboardRoutes:

    def test_index_returns_html(self, client):
        resp = client.get('/')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

    def test_index_contains_chart_data(self, app, client):
        ctx = {}
        def record(sender, template, context, **extra):
            ctx['chart_data'] = json.loads(context['chart_data'])
        template_rendered.connect(record, app)
        client.get('/')
        assert 'labels' in ctx['chart_data']
        assert 'data' in ctx['chart_data']
        template_rendered.disconnect(record, app)

    def test_index_contains_products(self, app, client, products):
        ctx = {}
        def record(sender, template, context, **extra):
            ctx['products'] = context['products']
        template_rendered.connect(record, app)
        client.get('/')
        assert len(ctx['products']) == 4
        template_rendered.disconnect(record, app)

    def test_index_contains_transactions(self, app, client, transaction_with_items):
        ctx = {}
        def record(sender, template, context, **extra):
            ctx['txs'] = list(context['transactions'])
        template_rendered.connect(record, app)
        client.get('/')
        assert len(ctx['txs']) == 1
        template_rendered.disconnect(record, app)

    def test_chart_returns_html(self, client):
        resp = client.get('/chart')
        assert resp.status_code == 200
        assert resp.mimetype == 'text/html'

    def test_chart_data_returns_200(self, client):
        resp = client.get('/chart/data')
        assert resp.status_code == 200

    def test_chart_data_has_labels(self, client):
        resp = client.get('/chart/data')
        data = resp.get_json()
        assert 'labels' in data
        assert len(data['labels']) == 7

    def test_chart_data_has_data(self, client):
        resp = client.get('/chart/data')
        data = resp.get_json()
        assert 'data' in data
        assert len(data['data']) == 7
        for val in data['data']:
            assert isinstance(val, float)

    def test_chart_data_reflects_transaction(self, app, client, db, transaction_with_items):
        with app.app_context():
            today = datetime.utcnow().date()
            transaction_with_items.created_at = datetime(today.year, today.month, today.day)
            db.session.commit()
        resp = client.get('/chart/data')
        data = resp.get_json()
        assert data['data'][6] == 17.0
