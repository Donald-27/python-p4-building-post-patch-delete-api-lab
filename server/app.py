#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'


@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(bakeries, 200)


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if not bakery:
        return make_response({'error': 'Bakery not found'}, 404)
    return make_response(bakery.to_dict(), 200)


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response([bg.to_dict() for bg in baked_goods], 200)


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if not most_expensive:
        return make_response({'error': 'No baked goods found'}, 404)
    return make_response(most_expensive.to_dict(), 200)


# ✅ POST /baked_goods
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    if not all([name, price, bakery_id]):
        return make_response({'error': 'Missing form data'}, 400)

    new_bg = BakedGood(name=name, price=float(price), bakery_id=int(bakery_id))
    db.session.add(new_bg)
    db.session.commit()

    return make_response(new_bg.to_dict(), 201)


# ✅ PATCH /bakeries/<int:id>
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response({'error': 'Bakery not found'}, 404)

    name = request.form.get('name')
    if name:
        bakery.name = name
        db.session.commit()

    return make_response(bakery.to_dict(), 200)


# ✅ DELETE /baked_goods/<int:id>
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    bg = BakedGood.query.get(id)
    if not bg:
        return make_response({'error': 'Baked good not found'}, 404)

    db.session.delete(bg)
    db.session.commit()
    return make_response({'message': 'Baked good successfully deleted'}, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
