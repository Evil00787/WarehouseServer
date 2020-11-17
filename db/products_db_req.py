from bson import ObjectId

from scripts.db.mongo_req import insert, select, update, delete, select_one
from scripts.model.product import db_product_id, to_dict, Product, db_quantity

global products


def add_product(item):
	if hasattr(item, 'price'):
		item.price = round(item.price, 2)
	response = insert(products, to_dict(item))
	item.pid = response.inserted_id
	return item


def remove_product(pid):
	return delete(products, {db_product_id: pid})


def update_product(product):
	if hasattr(product, 'price'):
		product.price = round(product.price, 2)
	data = to_dict(product)
	del data[db_product_id]
	data = {'$set': data}
	return update(products, {db_product_id: product.pid}, data)


def change_quantity(product):
	actual_product = get_product(product.pid)
	if actual_product[db_quantity] + product.quantity < 0:
		return False
	data = to_dict(product)
	del data[db_product_id]
	data = {'$inc': data}
	update(products, {db_product_id: product.pid}, data)
	actual_product[db_quantity] = actual_product[db_quantity] - product.quantity
	return actual_product


def get_product(pid):
	json = select_one(products, constraints={db_product_id: ObjectId(pid)})
	product = Product(json)
	return to_dict(product)


def get_products():
	jsons = select(products)
	dicts = []
	for json in jsons:
		dicts.append(to_dict(Product(json)))
	return dicts
