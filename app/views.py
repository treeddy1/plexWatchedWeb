from flask import render_template, request, redirect, url_for, flash
#from app import app, PLEX_SERVERS, MYSICKBEARD, MYSABNZBD, LOG_READER
from app import app, PLEX_SERVERS, MYSICKBEARD, MYSABNZBD, LOG_READER, db
from media import Show, Episode, Movie
import os
import shutil

@app.route('/')
@app.route('/index')
def index(type = ""):
	sb_fails = MYSICKBEARD.find_not_downloaded()
	sab_fails = MYSABNZBD.get_history_fail()
	shows = db.session.query(Episode.showName)

	return render_template('index.html', shows = shows, 
		episodes = Episode.query.all(), movies = Movie.query.all())

@app.route('/shows')
@app.route('/shows/<all>')
def shows(all = False):
	shows = PLEX_SERVERS.showList
	if all:
		all = True
	return render_template('index.html', shows = PLEX_SERVERS.showList, episodes = PLEX_SERVERS.episodeList, all = all)


@app.route('/movies')
@app.route('/movies/<all>')
def movies(all = False):
	if all:
		all = True
	return render_template('index.html', movies = PLEX_SERVERS.movieList, all = all)

@app.route('/show/<id>')
def show(id):
	myShow = []
	myShow = [show for show in PLEX_SERVERS.showList if show.id == id]
	return render_template('show.html', shows = myShow, episodes = PLEX_SERVERS.episodeList, all = True)

@app.route('/movie/<id>')
def movie(id):
	myMovie	 = PLEX_SERVERS.movieList[id]
	return render_template('movie.html', movie = myMovie)

@app.route('/update')
def update():
	#PLEX_SERVERS.clear_lists()
	PLEX_SERVERS.get_movies()
	PLEX_SERVERS.get_shows()
	return redirect(url_for('index'))



@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		delete_items = request.values
		for item in delete_items.keys():
			if "episode" in item:
				episode_id = delete_items[item]
				episode = PLEX_SERVERS.episodeList[episode_id]
				message = "Removing: {0}".format(episode.filePath)
				app.logger.info(message)
				if os.path.isfile(episode.filePath):
					os.remove(episode.filePath)
					del PLEX_SERVERS.episodeList[episode_id]
					message = "{0}: {1} was deleted!".format(episode.showName, episode.name)
					flash(message, 'success')
					app.logger.info("Deleted episode: {0} from disk".format(episode.filePath))
				else:
					message = "File not found {0}".format(episode.filePath)
					app.logger.error(message)
					flash(message, 'error')
		
			elif "movie" in item:
				movie_id = delete_items[item]
				movie = PLEX_SERVERS.movieList[movie_id]
				if movie.id == delete_items[item]:
					message = "Removing: {0}".format(movie.name)
					app.logger.info(message)
					if os.path.isfile(movie.filePath):
						path = os.path.dirname(movie.filePath)
						shutil.rmtree(path, ignore_errors=False)
						del PLEX_SERVERS.movieList[movie.id]
						app.logger.info("Deleted movie: {1} from disk".format(movie.filePath))
					else:
						message = "File not Found: {0}".format(movie.filePath)
						app.logger.error(message)
						flash(message, 'error')

	PLEX_SERVERS.refesh_library()
	return redirect(url_for('index'))


@app.route('/sickbeard')
@app.route('/sickbeard/<item_limit>')
def sickbeard(item_limit=20):
	sb_fails = MYSICKBEARD.find_not_downloaded(item_limit)
	return render_template('sickbeard.html', sb_fails=sb_fails)

@app.route('/sabnzbd')
@app.route('/sabnzbd/<item_limit>')
def sabnzbd(item_limit=20):
	sab_fails = MYSABNZBD.get_history_fail(item_limit)
	return render_template('sabnzbd.html', sab_fails=sab_fails)


@app.route('/config', methods=['GET', 'POST'])
def config():
	if request.method == 'POST':
		for item in request.values:
				print item + " : " + request.values[item]

	return render_template('config.html', config=app.config)

@app.route('/log')
@app.route('/log/<min_level>')
def log(min_level="ERROR"):
	lines = LOG_READER.read_log(min_level)
	return render_template('log.html', lines = lines)




