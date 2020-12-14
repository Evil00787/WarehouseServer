def select(collection, constraints=None):
	cursor = collection.find(constraints)
	json_docs = list(cursor)
	return json_docs


def select_one(collection, constraints=None):
	val = collection.find_one(constraints)
	return val


def insert(collection, data):
	return collection.insert_one(data)


def update(collection, id_filter, data):
	return collection.update_one(id_filter, data)


def delete(collection, constraints):
	return collection.delete_one(constraints)


def unpack_fields(fields):
	dict = {}
	if fields is None:
		return dict
	for field in fields:
		dict[fields] = 1
	return dict