from bson import ObjectId

db_product_id = "_id"
db_manufacturer = "manufacturerName"
db_model = "modelName"
db_price = "price"
db_quantity = "quantity"


def to_dict(product):
	dict = {}
	if hasattr(product, 'pid'):
		dict[db_product_id] = str(product.pid)
	if hasattr(product, 'manufacturer'):
		dict[db_manufacturer] = product.manufacturer
	if hasattr(product, 'model'):
		dict[db_model] = product.model
	if hasattr(product, 'price'):
		dict[db_price] = product.price
	if hasattr(product, 'quantity'):
		dict[db_quantity] = product.quantity
	return dict


class Product:
	def __init__(self, json_doc):
		if db_product_id in json_doc:
			self.pid = ObjectId(json_doc[db_product_id])
		if db_manufacturer in json_doc:
			self.manufacturer = json_doc[db_manufacturer]
		if db_model in json_doc:
			self.model = json_doc[db_model]
		if db_price in json_doc:
			self.price = json_doc[db_price]
		if db_quantity in json_doc:
			self.quantity = json_doc[db_quantity]
