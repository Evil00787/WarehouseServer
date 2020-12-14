from flask import render_template, jsonify, request, abort, Blueprint

from scripts.model.product import Product
from scripts.model import product as pr
from scripts.db import products_db_req as pdb
from scripts.model.user import ADMIN, Roles, MANAGER
from scripts.routes.auth import login_required

mainb = Blueprint('main', __name__)
success = {"success": True}

@mainb.route('/')
@login_required(role="ANY")
def default():
	return render_template('index.html')


@mainb.route('/products/all', methods=['GET'])
@login_required(role="ANY")
def get_products():
	doc = pdb.get_products()
	return jsonify(doc), 200


@mainb.route('/products', methods=['POST'])
@login_required(role="ANY")
def add_product():
	if not request.json or pr.db_manufacturer not in request.json or pr.db_model not in request.json or pr.db_price not in request.json:
		abort(400)
	product = Product(request.json)
	product = pdb.add_product(product)
	return jsonify(pr.to_dict(product)), 201


@mainb.route('/products/<string:idx>', methods=['PUT'])
@login_required(role="ANY")
def update_product(idx):
	if not request.json or pr.db_manufacturer not in request.json or pr.db_model not in request.json or pr.db_price not in request.json:
		abort(400)
	doc = pdb.get_product(idx)
	if doc is None:
		return jsonify({"error": "Product not found"}), 404
	temp = request.json
	temp[pr.db_product_id] = idx
	product = Product(temp)
	pdb.update_product(product)
	return jsonify(pr.to_dict(product)), 201


@mainb.route('/products/<string:idx>', methods=['PATCH'])
@login_required(role="ANY")
def update_quantity(idx):
	if not request.json or pr.db_quantity not in request.json:
		abort(400)
	temp = request.json
	temp[pr.db_product_id] = idx
	product = Product(temp)
	output = pdb.change_quantity(product)
	if isinstance(output, bool):
		return jsonify({"error": "Quantity can't be negative"}), 406
	return jsonify(pr.to_dict(output)), 204


@mainb.route('/products/<string:idx>', methods=['DELETE'])
@login_required(role=[str(Roles[ADMIN]), str(Roles[MANAGER])])
def delete_product(idx):
	doc = pdb.get_product(idx)
	if doc is None:
		return jsonify({"error": "Product not found"}), 404
	pdb.remove_product(idx)
	return jsonify(success), 201


@mainb.route('/products/<string:idx>', methods=['GET'])
@login_required(role="ANY")
def get_product(idx):
	doc = pdb.get_product(idx)
	if doc is None:
		abort(400)
	return jsonify(doc), 200
