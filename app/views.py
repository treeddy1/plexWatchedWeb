from flask import render_template, request, redirect, url_for, flash
from app import app, MYPLEX, MYSICKBEARD, MYSABNZBD
import os, time, shutil

@app.route('/')
@app.route('/index')
def index(type = ""):
	sb_fails = MYSICKBEARD.find_not_downloaded()
	sab_fails = MYSABNZBD.get_history_fail()

	return render_template('index.html', shows = MYPLEX.showList, movies = MYPLEX.movieList, sb_fails = sb_fails, sab_fails = sab_fails)

@app.route('/shows')
@app.route('/shows/<all>')
def shows(all = False):
	shows = MYPLEX.showList
	if all:
		all = True
	return render_template('index.html', shows = MYPLEX.showList, all = all)


@app.route('/movies')
@app.route('/movies/<all>')
def movies(all = False):
	if all:
		all = True
	return render_template('index.html', movies = MYPLEX.movieList, all = all)

@app.route('/show/<id>')
def show(id):
	myShow = []
	myShow = [show for show in MYPLEX.showList if show.id == id]
	return render_template('show.html', shows = myShow, all = True)

@app.route('/movie/<id>')
def movie(id):
	myMovie = next(movie for movie in MYPLEX.movieList if movie.id == id)
	return render_template('movie.html', movie = myMovie)

@app.route('/update')
def update():
	MYPLEX.movieList[:] = []
	MYPLEX.showList[:] =[]
	MYPLEX.get_movies()
	MYPLEX.get_shows()
	return redirect(url_for('index'))



@app.route('/delete', methods=['GET', 'POST'])
def delete():
	if request.method == 'POST':
		delete_items = request.values
		for item in delete_items.keys():
			if "episode" in item:
				shows = MYPLEX.showList
				for show in shows:
					for episode in show.episodes:
						if episode.id == delete_items[item]:
							print "Removing: " + episode.filePath
							try:
								if os.path.isfile(episode.filePath):
									os.remove(episode.filePath)
									show.episodes.remove(episode)
									#app.logger.info("Deleted episode: " + episode.filePath + "from disk")
								else:
									message = "Error: %s file not found" % episode.filePath
									print(message)
									flash(message, 'error')
							except:
								pass


			elif "movie" in item:
				item_id = delete_items[item]
				movie = next(tmp_movie for tmp_movie in MYPLEX.movieList if tmp_movie.id == item_id)
				if movie.id == delete_items[item]:
					print "Removing: " + movie.name
					try:
						if os.path.isfile(movie.filePath):
							path = os.path.dirname(movie.filePath)
							shutil.rmtree(path, ignore_errors=False)
							MYPLEX.movieList.remove(movie)
							#app.logger.info("Deleted movie: " + movie.filePath + "from disk")
						else:
							message = "Error: %s file not found" % movie.filePath
							print(message)
							flash(message, 'error')
					except:
						pass
				
	MYPLEX.refesh_library()
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


