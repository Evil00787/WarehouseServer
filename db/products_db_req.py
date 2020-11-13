from bson import ObjectId

from scripts.db.mongo_req import insert, select, update, delete, select_one
from scripts.model.product import db_product_id, to_dict, Product

global products


def add_product(item):
	response = insert(products, to_dict(item))
	item.pid = response.inserted_id
	return item


def remove_product(pid):
	return delete(products, {db_product_id: pid})


def update_product(product):
	data = to_dict(product)
	del data[db_product_id]
	return update(products, {db_product_id: product.pid}, data)


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
