from bson import ObjectId
from werkzeug.security import generate_password_hash

from scripts.db.mongo_req import insert, select, update, delete, select_one
from scripts.model.user import db_user_id, User, to_dict, db_login

global users


def get_user_by_id(uid):
	json = select_one(users, constraints={db_user_id: ObjectId(uid)})
	if json is None:
		return
	user = User(json)
	return user


def get_user_by_login(login):
	json = select_one(users, constraints={db_login: login})
	if json is None:
		return
	user = User(json)
	return user


def add_user(user):
	user.password = generate_password_hash(user.password, method='sha256')
	response = insert(users, to_dict(user))
	user.uid = response.inserted_id
	return user
