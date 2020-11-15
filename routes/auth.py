from functools import wraps

from flask import jsonify, request, abort, Blueprint, current_app
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash

from scripts.db import auth_db_req as adr
from scripts.model import user as u
from scripts.model.user import User, Roles, EMPLOYEE, ADMIN

authb = Blueprint('auth', __name__)


def login_required(role="ANY"):
	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			if not current_user.is_authenticated or (current_user.role != role and role != "ANY"):
				return current_app.login_manager.unauthorized()
			return fn(*args, **kwargs)
		return decorated_view
	return wrapper


@authb.route('/login', methods=['POST'])
def login():
	if not request.json or u.db_login not in request.json or u.db_password not in request.json:
		abort(400)
	user = adr.get_user_by_login(request.json[u.db_login])
	if user is None or not check_password_hash(user.password, request.json[u.db_password]):
		return jsonify({"success": False}), 201
	login_user(user)
	send_user = user
	send_user.auth = None
	send_user.password = None
	send_user.is_active = None
	send_user.is_anonymous = None
	send_user.is_authenticated = None
	return jsonify(send_user.to_json()), 201


@authb.route("/register", methods=['POST'])
@login_required(role=str(Roles[ADMIN]))
def register():
	if not request.json or u.db_login not in request.json or u.db_password not in request.json:
		abort(400)
	login = request.json[u.db_login]
	if adr.get_user_by_login(login) is not None:
		return jsonify({"success": False}), 201
	new_user = User(request.json)
	new_user.role = Roles[EMPLOYEE]
	new_user = adr.add_user(new_user)
	login_user(new_user)
	return jsonify({"success": True}), 201


@authb.route("/logout", methods=['GET'])
@login_required(role="ANY")
def logout():
	logout_user()
	return jsonify({"success": True}), 201
