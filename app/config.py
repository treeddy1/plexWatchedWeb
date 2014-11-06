import ConfigParser, os, app

# File no longer in use, leaving for documentatoin reasons 9/19/14
def get_config():

	if not os.path.isfile("config.ini"):
		print "Config file does not exist!"
		#create_config()
		return
	config = ConfigParser.ConfigParser()
	config.read("config.ini")
	app.config.update(
		IP = config.get('pww', 'ip'),
		PORT = config.get('pww', 'port'),
		DEBUG = config.get('pww', 'debug'),
		PLEX_USER = config.get('plex', 'user'),
		PLEX_PASSWORD = config.get('plex', 'password'),
		PLEX_HOST = config.get('plex', 'host')
	)

	"""['IP'] = config.get('pww', 'ip')
	app.config['PORT'] = config.get('pww', 'port')
	app.config['DEBUG'] = config.get('pww', 'debug')
	app.config['PLEX_USER'] = config.get('plex', 'user')
	app.config['PLEX_PASSWORD'] = config.get('plex', 'password')
	app.config['PLEX_HOST'] = config.get('plex', 'host')
	"""
	
def create_config():
	print "Creating config.ini"
	config = ConfigParser.ConfigParser()
	configFile = open('config.ini', 'wb+')
	config.add.section('pww')
	config.set('pww', 'ip', '0.0.0.0')
	config.set('pww', 'port', '3333')
	config.add_section('plex')
	config.set('plex', 'host', '127.0.0.1:32400')
	config.set('plex', 'user', '')
	config.set('plex', 'password', '')
	config.write(configFile)
	configFile.close()


