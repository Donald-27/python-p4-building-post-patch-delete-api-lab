#!/usr/bin/env python3

from app import app
from models import db, Bakery, BakedGood

with app.app_context():
    BakedGood.query.delete()
    Bakery.query.delete()
    
    b1 = Bakery(name='Delightful donuts')
    b2 = Bakery(name='Incredible crullers')
    db.session.add_all([b1, b2])

    g1 = BakedGood(name='Chocolate dipped donut', price=2.75, bakery=b1)
    g2 = BakedGood(name='Apple-spice filled donut', price=3.50, bakery=b1)
    g3 = BakedGood(name='Glazed honey cruller', price=3.25, bakery=b2)
    g4 = BakedGood(name='Chocolate cruller', price=3.40, bakery=b2)

    db.session.add_all([g1, g2, g3, g4])
    db.session.commit()
