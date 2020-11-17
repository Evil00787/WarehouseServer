from scripts import get_app

if __name__ == "__main__":
	get_app().run(debug=True, ssl_context=('cert.pem', 'key.pem'))
