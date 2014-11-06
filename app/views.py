from flask import render_template, request, redirect, url_for, flash
from app import app, MYPLEX, MYSICKBEARD, MYSABNZBD
import os, time, shutil

@app.route('/')
@app.route('/index')
def index(type = ""):
	shows = MYPLEX.get_shows()
	movies = MYPLEX.get_movies()
	sb_fails = MYSICKBEARD.find_not_downloaded()
	sab_fails = MYSABNZBD.get_history_fail()

	return render_template('index.html', shows = shows, movies = movies, sb_fails = sb_fails, sab_fails = sab_fails)

@app.route('/shows')
@app.route('/shows/<all>')
def shows(all = False):
	shows = MYPLEX.get_shows()
	if all:
		all = True
	return render_template('index.html', shows = shows, all = all)


@app.route('/movies')
@app.route('/movies/<all>')
def movies(all = False):
	movies = MYPLEX.get_movies()
	if all:
		all = True
	return render_template('index.html', movies = movies, all = all)


@app.route('/show/<id>')
def show(id):
	myShow = []
	shows = MYPLEX.get_shows()
	for show in shows:
		if show.id == id:
			myShow.append(show)
	return render_template('show.html', shows = myShow, all = True)


@app.route('/movie/<id>')
def movie(id):
	movies = MYPLEX.get_movies()
	for movie in movies:
		if movie.id == id:
			myMovie = movie
			#MYPLEX.get_plex_images(movie)
	return render_template('movie.html', movie = myMovie)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		delete_items = request.values
		for item in delete_items.keys():
			if "episode" in item:
				shows = MYPLEX.get_shows()
				for show in shows:
					for episode in show.episodes:
						if episode.id == delete_items[item]:
							print "Removing: " + episode.filePath
							if os.path.isfile(episode.filePath):
								os.remove(episode.filePath)
								#app.logger.info("Deleted episode: " + episode.filePath + "from disk")
							else:
								message = "Error: %s file not found" % episode.filePath
								print(message)
								flash(message, 'error')


			elif "movie" in item:
				movies = MYPLEX.get_movies()
				for movie in movies:
					if movie.id == delete_items[item]:
							print "Removing: " + movie.name
							if os.path.isfile(movie.filePath):
								#os.remove(movie.filePath)
								path = os.path.dirname(movie.filePath)
								#os.rmdir(path)
								shutil.rmtree(path, ignore_errors=False)
								#app.logger.info("Deleted movie: " + movie.filePath + "from disk")
							else:
								message = "Error: %s file not found" % movie.filePath
								print(message)
								flash(message, 'error')
				
	MYPLEX.refesh_library()
	time.sleep(.5)
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


