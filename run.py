from app import app


if __name__ == '__main__':
	app.run(app.config['IP'], port=app.config['PORT'], debug=True)


