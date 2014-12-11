import logging
from flask import Flask
from plex import Plex
from sickbeard import SickBeard
from sabnzbd import Sabnzbd
from timeit import Timer


# Create application
app = Flask(__name__)

# Setup Default Configuration
app.config.from_object('app.default_settings')

# Overide Defaults with configuration file
app.config.from_pyfile('application.cfg', silent=True)

# Set Secret key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Initiate logging
LOG_FILE = app.config['LOG_FILE']
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.ERROR)

# Load Plex configuration
PLEX_USER = app.config['PLEX_USER']
PLEX_PASSWORD = app.config['PLEX_PASSWORD']
PLEX_HOST = app.config['PLEX_HOST']

# Load SickBeard Configuration
SB_APIKEY = app.config['SB_APIKEY']
SB_HOST = app.config['SB_HOST']

# Load Sabnzbd Configuration
SABNZBD_APIKEY = app.config['SABNZBD_APIKEY']
SABNZBD_HOST = app.config['SABNZBD_HOST']

# Create Plex Object
MYPLEX = Plex(PLEX_HOST, PLEX_USER, PLEX_PASSWORD)
MYPLEX.get_shows()
MYPLEX.get_movies()

# Create SB Object
MYSICKBEARD = SickBeard(SB_HOST, SB_APIKEY)

# Create SABNZBD OBJECT
MYSABNZBD = Sabnzbd(SABNZBD_HOST, SABNZBD_APIKEY)

# Import HTML Views
from app import views



