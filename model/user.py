from json import JSONEncoder


def _default(self, obj):
	return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

db_user_id = "_id"
db_login = "login"
db_password = "password"
db_role = "role"
db_auth = "authenticationID"
active = 'is_active'
authenticated = 'is_authenticated'
anonymous = 'is_anonymous'
MANAGER = 'MANAGER'
EMPLOYEE = 'EMPLOYEE'
ADMIN = 'ADMIN'

Roles = {MANAGER: 0, EMPLOYEE: 1, ADMIN: 2}


def to_dict(user):
	dict = {}
	if hasattr(user, 'uid'):
		dict[db_user_id] = str(user.uid)
	if hasattr(user, 'login'):
		dict[db_login] = str(user.login)
	if hasattr(user, 'password'):
		dict[db_password] = str(user.password)
	if hasattr(user, 'role'):
		dict[db_role] = str(user.role)
	if hasattr(user, 'auth'):
		dict[db_auth] = str(user.auth)
	if hasattr(user, active):
		dict[active] = str(user.is_active)
	if hasattr(user, authenticated):
		dict[authenticated] = str(user.is_authenticated)
	if hasattr(user, anonymous):
		dict[anonymous] = str(user.is_anonymous)
	return dict


class User:
	def __init__(self, json_doc):
		if db_user_id in json_doc:
			self.uid = json_doc[db_user_id]
		if db_login in json_doc:
			self.login = json_doc[db_login]
		if db_password in json_doc:
			self.password = json_doc[db_password]
		if db_role in json_doc:
			self.role = json_doc[db_role]
		if db_auth in json_doc:
			self.auth = json_doc[db_auth]
		self.is_active = True
		self.is_authenticated = True
		self.is_anonymous = False
		super().__init__()

	def get_id(self):
		return str(self.uid)

	def to_json(self):
		ret = to_dict(self)
		return ret
