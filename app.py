import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/api/search')
def search():
    q = request.args.get('q', '')
    results = Product.query.filter(Product.name.contains(q)).all()
    data = [{'id': p.id, 'name': p.name, 'price': p.price} for p in results]
    return jsonify(data)

def seed_data():
    if Product.query.count() == 0:
        db.session.add(Product(name='iPhone 18 Pro', price=1299, category='phones'))
        db.session.add(Product(name='سيارة 2026', price=28500, category='cars'))
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
