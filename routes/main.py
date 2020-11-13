from flask import render_template, jsonify, request, abort, Blueprint

from scripts.model.product import Product
from scripts.model import product as pr
from scripts.db import products_db_req as pdb
from scripts.routes.auth import login_required

mainb = Blueprint('main', __name__)


@mainb.route('/')
@login_required(role="ANY")
def default():
	return render_template('index.html')


@mainb.route('/products', methods=['GET'])
@login_required(role="ANY")
def get_products():
	doc = pdb.get_products()
	return jsonify(doc), 200


@mainb.route('/product/add', methods=['POST'])
@login_required(role="ANY")
def add_product():
	if not request.json or pr.db_manufacturer not in request.json or pr.db_model not in request.json or pr.db_price not in request.json:
		abort(400)
	product = Product(request.json)
	product = pdb.add_product(product)
	return jsonify(pr.to_dict(product)), 201


@mainb.route('/product/update', methods=['POST'])
@login_required(role="ANY")
def update_product():
	if not request.json or pr.db_product_id not in request.json or pr.db_manufacturer not in request.json or pr.db_model not in request.json or pr.db_price not in request.json:
		abort(400)
	product = Product(request.json)
	pdb.update_product(product)
	return jsonify(pr.to_dict(product)), 201


@mainb.route('/product', methods=['GET'])
@login_required(role="ANY")
def get_product():
	if not request.json or pr.db_product_id not in request.json:
		abort(400)
	doc = pdb.get_product(request.json[pr.db_product_id])
	return jsonify(doc), 200
